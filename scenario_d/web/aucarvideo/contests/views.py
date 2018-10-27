# -*- coding: utf-8 -*-

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
# from django.core.mail import send_mail
# from django.db import transaction
# from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404

from contests.forms import ContestCreateForm
from contests.forms import ContestUpdateForm
from contests.forms import VideoForm
from contests.models import DynamoContestManager
from contests.models import DynamoVideoManager


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


class ContestAdminCreate(FormView):

    template_name = 'contests/contest_form.html'
    form_class = ContestCreateForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        name = form.cleaned_data['name']
        url = slugify(name)
        image = self.request.FILES['image']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        award_description = form.cleaned_data['award_description']
        
        try:
            manager = DynamoContestManager()
            company = manager.create_contest(
                company_name=self.request.user.company_name, 
                contest_name=name,
                image=image,
                url=url,
                start_date=start_date,
                end_date=end_date,
                award_description=award_description,
            )
            messages.success(self.request,'El concurso fue creado con exito')
        except Exception as e:
            messages.warning(self.request,str(e))

        return HttpResponseRedirect(reverse('contests:contest_admin_list'))


class ContestAdminList(TemplateView):

    def get(self, request, *args, **kwargs):
        manager = DynamoContestManager()
        # Getting the company data as a Python dict
        # Ex: {'Contests': {}, 'Name': 'company2'}
        data = manager.get_contests(
            company_name=request.user.company_name
        )

        contests_dict = data.get('Contests')
        ordered_contests = sorted(contests_dict.items(), key=lambda x: int(x[1]['Start_date'].replace('-','')))

        # Show 23 contacts per page
        paginator = Paginator(ordered_contests, 1)

        page = request.GET.get('page')
        object_list = paginator.get_page(page)

        template_name = 'contests/contest_admin_list.html'
        context = {
            'is_paginated': True,
            'object_list': object_list
        }
        return render(request,template_name,context)


class ContestAdminUpdate(FormView):

    template_name = 'contests/contest_form.html'
    form_class = ContestUpdateForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ContestAdminUpdate, self).get_initial()

        company_name = self.request.user.company_name
        contest_url = self.kwargs.get('url')

        manager = DynamoContestManager()
        contest = manager.get_contest_by_url(company_name,contest_url)

        # If the contest with 'contest_url' is not found. The 
        # server will raise a 404 error
        if not contest:
            raise Http404(f'Concurso {contest_url} no encontrado')

        contest_name, contest_data = contest

        initial['name'] = contest_name
        initial['url'] = contest_data.get('Url')
        initial['start_date'] = contest_data.get('Start_date')
        initial['end_date'] = contest_data.get('End_date')
        initial['award_description'] = contest_data.get('Award_description')

        initial['s3_image_url'] = contest_data.get('Image_url')

        # If the contest os not found we will return a 404 error
        return initial

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        image = self.request.FILES['image'] if 'image' in self.request.FILES else None
        s3_image_url = form.cleaned_data['s3_image_url']

        url = slugify(form.cleaned_data['url'])
        name = form.cleaned_data['name']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        award_description = form.cleaned_data['award_description']
        
        try:
            manager = DynamoContestManager()
            company = manager.update_contest(
                company_name=self.request.user.company_name, 
                contest_name=name,
                image=image,
                new_image=image,
                # contest url
                url=url,
                image_url=s3_image_url,
                start_date=start_date,
                end_date=end_date,
                award_description=award_description,
                
                update=True
            )
            messages.success(self.request,f'El concurso {name} fue actualizado')
        except Exception as e:
            messages.warning(self.request,str(e))

        return HttpResponseRedirect(reverse('contests:contest_admin_list'))


class ContestAdminDetail(TemplateView):

    def get(self, request, *args, **kwargs):
        company_name = self.request.user.company_name
        contest_url = kwargs.get('url')
        c_manager = DynamoContestManager()
        data = c_manager.get_contest_by_url(company_name,contest_url)
        contest_name, contest_data = data
        # Traer los detalles del concurso 
        # Traer los videos del concurso
        # v_manager = DynamoVideoManager()
        # videos_dict = v_manager.get_videos(company_name,contest_name)

        template_name = 'contests/contest_admin_detail.html'
        context = {
            'contest' :{
                'name': contest_name,
                'award_description': contest_data.get('Award_description')
            }
        }
        return render(request,template_name,context)



class ContestAdminDelete(TemplateView):

    def get(self, request, *args, **kwargs):
        contest_url = self.kwargs.get('url')

        manager = DynamoContestManager()
        data = manager.get_contest_by_url(
            company_name=request.user.company_name,
            contest_url=contest_url
        )

        contest_name, contest_data = data
        template_name = 'contests/contest_confirm_delete.html'
        context = { 'contest_name':contest_name }

        return render(request,template_name,context)

    def post(self, request, *args, **kwargs):
        contest_url = self.kwargs.get('url')
        company_name = self.request.user.company_name
        manager = DynamoContestManager()
        status = manager.delete_contest_by_url(company_name,contest_url)
        if status == 200:
            messages.success(request,f'El consurso {contest_url} fue eliminado.')
            return HttpResponseRedirect(reverse('contests:contest_admin_list'))
        
        messages.error(request,f'El concurso {contest_url} no fue eliminado.')
        return HttpResponseRedirect(reverse('contests_contest_admin_list'))


@method_decorator(csrf_exempt, name='dispatch')
class VideoAdminCreate(FormView):

    template_name = 'contests/video_form.html'
    form_class = VideoForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(VideoAdminCreate, self).get_initial()
        # initial['contest_name'] = 

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        company_name=self.request.user.company_name
        contest_name = self.kwargs.get('name')

        video = form.cleaned_data['video']
        p_fname = form.cleaned_data['participant_fname']
        p_lname = form.cleaned_data['participant_lname']
        p_email = form.cleaned_data['participant_email']
        description = form.cleaned_data['description']
        status = 'Processing..'

        manager = DynamoVideoManager()
        status = manager.create_video(
            company_name=company_name,
            contest_name=contest_name,
            video=video,
            description=description,
            status=status,
            p_fname=p_fname,
            p_lname=p_lname,
            p_email=p_email
        )

        if status == 200:
            messages.success(self.request,f'El video {video.name} fue creado.')
        else:
            messages.error(self.request,f'El video {video.name} no fue creado.')

        return HttpResponseRedirect(reverse('contests:video_admin_list'))


# class VideoAdminList(TemplateView):

#     def get(self, request, *args, **kwargs):


#         contests_dict = data.get('Contests')
#         ordered_contests = sorted(contests_dict.items(), key=lambda x: int(x[1]['Start_date'].replace('-','')))

#         # Show 23 contacts per page
#         paginator = Paginator(ordered_contests, 1)

#         page = request.GET.get('page')
#         object_list = paginator.get_page(page)

#         template_name = 'contests/contest_admin_list.html'
#         context = {
#             'is_paginated': True,
#             'object_list': object_list
#         }
#         return render(request,template_name,context)

#     def get(self, request, *args, **kwargs):
#         manager = DynamoVideoManager()
#         data = manager.get_videos(
#             company_name=request.user.company_name
#             contest_name=
#         )

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


