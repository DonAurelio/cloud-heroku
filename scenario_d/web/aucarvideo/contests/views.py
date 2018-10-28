# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.conf import settings
from django.core.mail import send_mail

from contests.forms import ContestCreateForm
from contests.forms import ContestUpdateForm
from contests.forms import VideoForm
from contests.models import DynamoContestManager
from contests.models import DynamoVideoManager

from aucarvideo.celery import app as celery_app

import re
import logging
import datetime


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
        paginator = Paginator(ordered_contests, settings.PAGINATION_BY)

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
        
        # try:
        manager = DynamoContestManager()
        company = manager.update_contest(
            company_name=self.request.user.company_name, 
            contest_name=name,
            new_image=image,
            # contest url
            url=url,
            image_url=s3_image_url,
            start_date=start_date,
            end_date=end_date,
            award_description=award_description
        )
        messages.success(self.request,f'El concurso {name} fue actualizado')
        # except Exception as e:
        #     messages.warning(self.request,str(e))

        return HttpResponseRedirect(reverse('contests:contest_admin_list'))


class ContestAdminDetail(TemplateView):
    """
    Display videos and data from a given contest for
    admin purposes.
    """

    def get(self, request, *args, **kwargs):
        company_name = self.request.user.company_name
        contest_url = kwargs.get('url')
        c_manager = DynamoContestManager()
        data = c_manager.get_contest_by_url(company_name,contest_url)
        contest_name, contest_data = data

        v_manager = DynamoVideoManager()
        object_list = v_manager.get_videos(company_name,contest_name)

        ordered_contests = sorted(
            object_list.items(), 
            key=lambda x: int(x[1].get('Uploaded_at','0').replace('-','')),
            reverse=True
        )

        # Show 23 contacts per page
        paginator = Paginator(ordered_contests, settings.PAGINATION_BY)

        page = request.GET.get('page')
        object_list = paginator.get_page(page)

        template_name = 'contests/contest_admin_detail.html'
        context = {
            'contest' :{
                'url': contest_url,
                'name': contest_name,
                'award_description': contest_data.get('Award_description')
            },
            'is_paginated': True,
            'object_list': object_list
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


class ContestPublicDetail(TemplateView):
    """
    Display videos and data from a given contest
    for public purposes
    """

    def get(self, request, *args, **kwargs):
        company_name = kwargs.get('company_name')
        contest_url = kwargs.get('contest_url')

        c_manager = DynamoContestManager()
        data = c_manager.get_contest_by_url(company_name,contest_url)
        contest_name, contest_data = data

        v_manager = DynamoVideoManager()
        object_list = v_manager.get_videos(company_name,contest_name)

        condition = lambda obj: 'Processing' not in obj[1]['Stat']
        object_list = list(filter(condition,object_list.items()))

        ordered_contests = sorted(
            object_list, 
            key=lambda x: int(x[1].get('Uploaded_at','0').replace('-','')),
            reverse=True
        )

        paginator = Paginator(ordered_contests, settings.PAGINATION_BY)

        page = request.GET.get('page')
        object_list = paginator.get_page(page)

        template_name = 'contests/contest_public_detail.html'
        context = {
            'company':{
                'name': company_name
            },
            'contest' :{
                'name': contest_name,
                'url': contest_url,
                'award_description': contest_data.get('Award_description')
            },
            'is_paginated': True,
            'object_list': object_list
        }
        return render(request,template_name,context)


@method_decorator(csrf_exempt, name='dispatch')
class VideoAdminCreate(FormView):

    template_name = 'contests/video_form.html'
    form_class = VideoForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(VideoAdminCreate, self).get_initial()

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        company_name=self.request.user.company_name
        contest_url = self.kwargs.get('url')

        manager = DynamoContestManager()
        contest_name, contest_data = manager.get_contest_by_url(company_name,contest_url)

        video = form.cleaned_data['video']
        p_fname = form.cleaned_data['participant_fname']
        p_lname = form.cleaned_data['participant_lname']
        p_email = form.cleaned_data['participant_email']
        description = form.cleaned_data['description']
        status = 'Converted' if 'mp4' in video.name else 'Processing'

        manager = DynamoVideoManager()
        obj_key, status = manager.create_video(
            company_name=company_name,
            contest_name=contest_name,
            video=video,
            description=description,
            uploaded_at=str(datetime.date.today()),
            status=status,
            p_fname=p_fname,
            p_lname=p_lname,
            p_email=p_email
        )

        if status == 200:
            messages.success(self.request,f'El video {video.name} fue creado.')

            mail = self.request.POST.get('send_mail',None)
            if mail:
                path = reverse(
                    'contests:contest_public_detail',
                    args=[company_name,contest_url]
                )
                web_url = settings.ELB_URL_FORMAT.format(path=path)

                self.send_mail(
                    video.name,
                    p_email,
                    web_url
                )

            if 'mp4' not in video.name:
                self.send_video_processing_job(
                    company_name,contest_name,video.name,obj_key,web_url,p_email
                )
        else:
            messages.error(self.request,f'El video {video.name} no fue creado.')

        return HttpResponseRedirect(reverse('contests:contest_admin_detail', args=[contest_url]))

    def send_mail(self, video_name, receiver, web_url):
    
        if 'mp4' in video_name:

            subject = 'Video Publicado'
            message = (
                f"Tu video {video_name} ha sido publicado en la página web"
                f"oficial del concursos {web_url}."
            )
        else:

            subject = 'Video en Procesamiento'
            message = (
                f"Hemos recibido tu video {video_name} y lo estamos procesando."
                "Apenas se encuentre disonible podras verlo en la página oficial"
                f"del concursos {web_url}."
            )


        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [receiver],
            fail_silently=False
        )

    def send_video_processing_job(self, company_name, contest_name, video_name, video_id, web_url,email_rcv):
        data = [company_name,contest_name,video_name,video_id, web_url,email_rcv]
        celery_app.send_task('tasks.process_video_from_s3',data)


@method_decorator(csrf_exempt, name='dispatch')
class VideoPublicCreate(FormView):

    template_name = 'contests/video_form.html'
    form_class = VideoForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        company_name = self.kwargs.get('company_name')
        contest_url = self.kwargs.get('contest_url')

        manager = DynamoContestManager()
        contest_name, contest_data = manager.get_contest_by_url(company_name,contest_url)

        video = form.cleaned_data['video']
        p_fname = form.cleaned_data['participant_fname']
        p_lname = form.cleaned_data['participant_lname']
        p_email = form.cleaned_data['participant_email']
        description = form.cleaned_data['description']
        status = 'Converted' if 'mp4' in video.name else 'Processing'

        manager = DynamoVideoManager()
        obj_key, status = manager.create_video(
            company_name=company_name,
            contest_name=contest_name,
            video=video,
            description=description,
            uploaded_at=str(datetime.date.today()),
            status=status,
            p_fname=p_fname,
            p_lname=p_lname,
            p_email=p_email
        )

        if status == 200:
            messages.success(self.request,f'El video {video.name} fue creado.')

            mail = self.request.POST.get('send_mail',None)
            if mail:
                path = reverse(
                    'contests:contest_public_detail',
                    args=[company_name,contest_url]
                )
                web_url = settings.ELB_URL_FORMAT.format(path=path)

                self.send_mail(
                    video.name,
                    p_email,
                    web_url
                )

            if 'mp4' not in video.name:
                self.send_video_processing_job(
                    company_name,contest_name,video.name,obj_key,web_url,p_email
                )
        else:
            messages.error(self.request,f'El video {video.name} no fue creado.')

        return HttpResponseRedirect(
            reverse('contests:contest_public_detail', args=[company_name,contest_url])
        )

    def send_mail(self,video_name, receiver, web_url):
    
        if 'mp4' in video_name:

            subject = 'Video Publicado'
            message = (
                f"Tu video {video_name} ha sido publicado en la página web"
                f"oficial del concursos {web_url}."
            )
        else:
            subject = 'Video en Procesamiento'
            message = (
                f"Hemos recibido tu video {video_name} y lo estamos procesando."
                "Apenas se encuentre disonible podras verlo en la página oficial"
                f"del concursos {web_url}."
            )

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [receiver],
            fail_silently=False
        )

    def send_video_processing_job(self, company_name, contest_name,video_name,video_id, web_url, email_rcv):
        data = [company_name,contest_name,video_name,video_id, web_url,email_rcv]
        celery_app.send_task('tasks.process_video_from_s3',data)


class VideoProcessingStatus(TemplateView):

    @csrf_exempt
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):

        company_name = request.POST.get('company_name')
        contest_name = request.POST.get('contest_name')
        video_name = request.POST.get('video_name')
        web_url = request.POST.get('web_url')
        video_id = request.POST.get('video_id')
        email_rcv = request.POST.get('email_rcv')

        manager = DynamoVideoManager()
        manager.update_video_status(company_name, contest_name, video_id)

        # Participants email notification
        subject = 'Video Publicado'
        message = (
            f"El video {video_name} ha sido publicado en la página web"
            f"oficial del concursos {web_url}."
        )
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email_rcv],
            fail_silently=False
        )

        return JsonResponse(data=None,status=200,safe=False)


