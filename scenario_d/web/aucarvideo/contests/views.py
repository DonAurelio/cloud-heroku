# from __future__ import absolute_import, unicode_literals
from aucarvideo.celery import app as celery_app

# from django.views.generic.edit import CreateView
# from django.views.generic.edit import DeleteView
# from django.views.generic.edit import UpdateView
# from django.views.generic.detail import DetailView
# from django.views.generic.list import ListView
# from django.views.generic import TemplateView
# from django.shortcuts import reverse, render
# from django.urls import reverse_lazy
# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.mail import send_mail
# from django.db import transaction
# from django.conf import settings

# from django.utils.decorators import method_decorator

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import reverse

from contests.forms import ContestForm

from profile.models import DynamoCompanyManager


import re
import logging


logger = logging.getLogger(__name__)

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


class ContestCreate(FormView):
    template_name = 'contest/contest_form.html'
    form_class = ContestForm
    # success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        name = form.cleaned_data['name']
        url = slugify(form.cleaned_data['url'])
        image = form.cleaned_data['image']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        award_description = form.cleaned_data['award_description']
        
        # SAVE IN DYNAMO

        return super().form_valid(form)

    def get_succces_url(self):
        return reverse('contests:contest_admin_list')


class ContestList(TemplateView):

    def get(self, request, *args, **kwargs):
        manager = DynamoCompanyManager()
        # Getting the company data as a Python dict
        company = manager.get_company(
            company_name=request.user.get_company
        )



# class ContestDetail(ListView):
#     """
#     View for contest detail, the contest
#     detail contains the contest itself and 
#     a list of videos that belongs to the contest.
#     """

#     model = Video
#     template_name = 'contests/contest_detail.html'
#     paginate_by = 50

#     def get_queryset(self):
#         """
#         Return videos filtered by contest
#         """
#         contest_url = self.kwargs.get('url')
#         videos = Video.objects.filter(contest__url=contest_url)
#         # If the video has URL it was already converted 
#         videos = [ video for video in videos if video.url ]
#         return videos

#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         contest_url = self.kwargs.get('url')
#         context['contest'] = Contest.objects.get(url=contest_url)
#         return context


# class ContestList(ListView):
#     """
#     View for contest objects listing 
#     for the general public.
#     """
#     model = Contest
#     # paginate_by = 1
#     template_name = 'contests/contest_list.html'

#     def get_queryset(self):
#         queryset = Contest.objects.filter(user=self.request.user)
#         return queryset


# class ContestUpdate(UpdateView):
#     model = Contest
#     fields = [
#         'name','banner','url',
#         'start_date','end_date',
#         'award_description'
#     ]

#     def form_valid(self, form):
#         """
#         The sistem creates automatically a URL 
#         for the contest.
#         """
#         contest = form.save()

#         # The URL assigned to the contest 
#         # is the name of the contests.
#         url = contest.url
#         contest.url = slugify(url)
#         contest.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def get_object(self):
#         """
#         Return the contest with the given URL.
#         """
#         return get_object_or_404(self.model, url=self.kwargs['url'])

#     def get_success_url(self):
#         return reverse('contests:contest_admin_list')


# class ContestDelete(DeleteView):
#     """
#     View for contest delection.
#     """
#     model = Contest
#     success_url = reverse_lazy('contests:contest_admin_list')


# class ContestAdminList(ListView):
#     """
#     View for contest objects listing 
#     for admin purposes.
#     """

#     model = Contest
#     paginate_by = 10
#     template_name = 'contests/contest_admin_list.html'


# @method_decorator(csrf_exempt, name='dispatch')
# class VideoCreate(TemplateView):
#     """
#     View for video objects creation.
#     """

#     # @csrf_exempt
#     def dispatch(self,request,*args,**kwargs):
#         return super().dispatch(request,*args,**kwargs)

#     def get(self,request,*args,**kwargs):
#         video_form = VideoForm()
#         participant_form = ParticipantForm()

#         template_name = 'contests/video_form.html'
#         context = {
#             'video_form': video_form,
#             'participant_form': participant_form
#         }

#         return render(request,template_name,context)

#     def post(self,request,*args,**kwargs):

#         video_form = VideoForm(request.POST,request.FILES)
#         participant_form = ParticipantForm(request.POST)

#         needs_send_mail = request.POST.get('send_mail',None)

#         if video_form.is_valid() and participant_form.is_valid():
#             participant = participant_form.save()
#             contest = Contest.objects.get(pk=kwargs.get('pk'))

           
#             try:


#                 # If some error happens during the processing 
#                 # of this block of code the database is 
#                 # rolled back, i.e, in case the email
#                 # sending fails or some process carried 
#                 # out on the following block of code.
#                 with transaction.atomic():

#                     video = video_form.save(commit=False)
#                     video.contest = contest
#                     video.participant = participant
#                     video.save()

#                     # If the uploaded video already has the .mp4
#                     # format it will not be converted.
#                     if '.mp4' in video.file.name:
#                         video.status = Video.CONVERTED
#                         video.save()

#                         # Participants email notification
#                         contest = video.contest.name.title()
#                         subject = f'Video Publicado'
#                         message = f"""
#                         Tu video '{video.name}' ha sido publicado
#                         directamente ya que cumple con el formato
#                         que requiere el concurso.
#                         """
#                     else:
#                         # Participants email notification
#                         contest = video.contest.name.title()
#                         subject = f'Video para Procesamiento'
#                         message = f"""
#                         Hemos recibido tu video '{video.name}' y los estamos  procesado para  
#                         que  sea  publicado. Tan  pronto el  video quede publicado 
#                         en la página del concurso te notificaremos por email.
#                         """

#                         video_id = video.id
#                         input_file = video.file.url
#                         output_file =  video.converted_url

#                         data = [
#                             video_id,
#                             input_file,
#                             output_file
#                         ]

#                         # Sending the videp processing job to the queue
#                         # celery_tasks.hello_world.delay()
#                         # celery_app.send_task(
#                         #     name='tasks.hello_world', 
#                         # )
#                         celery_app.send_task(
#                             'tasks.process_video',
#                             data
#                         )
                
#                     if needs_send_mail:
#                         send_mail(
#                             subject,
#                             message,
#                             settings.EMAIL_HOST_USER,
#                             [video.participant.email],
#                             fail_silently=False,
#                         )


#             except Exception as e:
#                 logger.exception(e)


#             current_contest_pk = kwargs.get('pk')

#             return HttpResponseRedirect(
#                 reverse('contests:video_admin_list', kwargs={'pk':current_contest_pk})
#             )

#         template_name = 'contests/video_form.html'
#         context = {
#             'video_form': video_form,
#             'participant_form': participant_form
#         }

#         return render(request,template_name,context)


# class VideoAdminList(ListView):
#     """
#     List videos for a given contest
#     for admin purposes. 
#     """

#     model = Video
#     template_name = 'contests/video_admin_list.html'
#     paginate_by = 50

#     def get_queryset(self):
#         """
#         Return videos filtered by contest
#         """
#         contest_pk = self.kwargs.get('pk')
#         videos = Video.objects.filter(contest__pk=contest_pk)
#         return videos

#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         contest_pk = self.kwargs.get('pk')
#         context['contest'] = Contest.objects.get(pk=contest_pk)
#         return context


# class VideoProcessingStatus(TemplateView):

#     @csrf_exempt
#     def dispatch(self,request,*args,**kwargs):
#         return super().dispatch(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         video_id = request.POST.get('video_id')
#         video_id = int(video_id)

#         video = Video.objects.get(id=video_id)
#         video.status = video.CONVERTED
#         video.save()

#         # Participants email notification
#         contest = video.contest.name.title()
#         subject = f'Video Publicado en {contest}'
#         message = f'El video {video.name} ha sido publicado satisfactoriamente'
        
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [video.participant.email],
#             fail_silently=False,
#         )

#         return JsonResponse(data=None,status=200,safe=False)


