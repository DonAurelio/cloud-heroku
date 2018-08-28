from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.shortcuts import reverse, render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from contests.models import Contest
from contests.models import Video

from contests.forms import VideoForm
from contests.forms import ParticipantForm

import re


# Reference: https://blog.dolphm.com/slugify-a-string-in-python/
def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)

    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)

    # "some articles title "
    # "some articles title"
    s = s.strip()

    # "some articles title"
    # "some-articles-title"
    s = s.replace(' ', '-')

    return s


class ContestCreate(CreateView):
    """
    View for contest objects creation.
    """
    model = Contest
    template_name = 'contests/contest_form.html'
    fields = [
        'name','banner',
        'start_date','end_date',
        'award_description'
    ]

    def form_valid(self, form):
        """
        The sistem creates automatically a URL 
        for the contest.
        """
        contest = form.save()

        # The URL assigned to the contest 
        # is the name of the contests.
        url = contest.name
        contest.url = slugify(url)
        contest.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        When the form is saved successfully 
        the get_success_url is called.
        """
        return reverse('contests:contest_admin_list')


class ContestDetail(DetailView):
    """
    View for contest detail for
    both purposes, admin and general public.
    """

    model = Contest
    template_name = 'contests/contest_detail.html'

    def get_object(self):
        """
        Return a the contest with the given URL.
        """
        return get_object_or_404(self.model, url=self.kwargs['url'])


class ContestList(ListView):
    """
    View for contest objects listing 
    for the general public.
    """
    model = Contest
    # paginate_by = 1
    template_name = 'contests/contest_list.html'


class ContestUpdate(UpdateView):
    model = Contest
    fields = [
        'name','banner','url',
        'start_date','end_date',
        'award_description'
    ]

    def form_valid(self, form):
        """
        The sistem creates automatically a URL 
        for the contest.
        """
        contest = form.save()

        # The URL assigned to the contest 
        # is the name of the contests.
        url = contest.url
        contest.url = slugify(url)
        contest.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        """
        Return the contest with the given URL.
        """
        return get_object_or_404(self.model, url=self.kwargs['url'])

    def get_success_url(self):
        return reverse('contests:contest_admin_list')


class ContestDelete(DeleteView):
    """
    View for contest delection.
    """
    model = Contest
    success_url = reverse_lazy('contests:contest_admin_list')


class ContestAdminList(ListView):
    """
    View for contest objects listing 
    for admin purposes.
    """

    model = Contest
    paginate_by = 10
    template_name = 'contests/contest_admin_list.html'

    # def get(self, request,*args,**kwargs):
    #     concursos = list()
    #     concursos = Contest.objects.all()

    #     concursos_ordenados = sorted(concursos, key=lambda x: x.start_date, reverse=True)

    #     template_name = 'contests/contest_admin_list.html'
    #     context = {
    #         'concursos': concursos_ordenados
    #     }

    #     return render(request, template_name, context)


class VideoCreate(TemplateView):
    """
    View for video objects creation.
    """

    def get(self,request,*args,**kwargs):
        video_form = VideoForm()
        participant_form = ParticipantForm()

        template_name = 'contests/video_form.html'
        context = {
            'video_form': video_form,
            'participant_form': participant_form
        }

        return render(request,template_name,context)

    def post(self,request,*args,**kwargs):
        video_form = VideoForm(request.POST,request.FILES)
        participant_form = ParticipantForm(request.POST)

        if video_form.is_valid() and participant_form.is_valid():
            participant = participant_form.save()
            contest = Contest.objects.get(pk=kwargs.get('pk'))

            video = video_form.save(commit=False)
            video.contest = contest
            video.participant = participant
            video.save()

            # If the uploaded video already has the .mp4
            # format it will not be converted.
            if '.mp4' in video.file.name:
                video.status = Video.CONVERTED
                video.save()
         

            current_contest_pk = kwargs.get('pk')
            return HttpResponseRedirect(
                reverse('contests:video_admin_list', kwargs={'pk':current_contest_pk})
            )

        template_name = 'contests/video_form.html'
        context = {
            'video_form': video_form,
            'participant_form': participant_form
        }

        return render(request,template_name,context)


class VideoAdminList(ListView):
    """
    List videos for a given contest
    for admin purposes. 
    """

    model = Video
    template_name = 'contests/video_admin_list.html'
    paginate_by = 50

    def get_queryset(self):
        """
        Return videos filtered by contest
        """
        contest_pk = self.kwargs.get('pk')
        videos = Video.objects.filter(contest__pk=contest_pk)
        return videos

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        contest_pk = self.kwargs.get('pk')
        context['contest'] = Contest.objects.get(pk=contest_pk)
        return context


class VideoProcessingStatus(TemplateView):

    def get(self,request,*args,**kwargs):
        pending_videos = Video.objects.filter(
            status=Video.PROCESSING,
        ).exclude(
            file__icontains='.mp4'
        )

        paths = []
        for video in pending_videos:
            data = (video.id,video.file.url, video.get_converted_url())
            paths.append(data)

        return JsonResponse(data=paths,safe=False)

    def post(self,request,*args,**kwargs):
        video_id = request.POST.get('id')
        processed_video_name = request.POST.get('name')

        return JsonResponse(data=None,status=200,safe=False)


