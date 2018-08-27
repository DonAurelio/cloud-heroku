from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.shortcuts import reverse, render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from contests.models import Contest
from contests.models import Video

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
        print('URL', self.model, self.kwargs, self.kwargs['url'], type(self.kwargs['url']))
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


class VideoAdminList(ListView):
    """
    List videos for a given contest
    for admin purposes. 
    """

    model = Video
    template_name = 'contests/video_admin_list.html'

    def get_queryset(self):
        """
        Return videos filtered by contest
        """
        contest_url = self.kwargs.get('url')
        videos = Video.objects.filter(contest__url=contest_url)
        return videos
