# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList

import datetime


class ContestCreateForm(forms.Form):
    name = forms.CharField(max_length=200)
    image = forms.FileField()
    # S3 image url
    s3_image_url = forms.CharField(max_length=200, widget=forms.HiddenInput())
    start_date = forms.DateField(
        help_text="Please use the following format: YYYY-MM-DD HH:MM:ss. e.g, 2018-08-14 22:10:24."
    )
    end_date = forms.DateField()
    award_description = forms.CharField(max_length=200)


    def clean(self):
        cleaned_data = super().clean()

        """Validate start date."""
        now = datetime.date.today()

        # Now datetime is naive, so it is localized
        # to the current user timezone.
        #now_aware = pytz.utc.localize(now)
        now_aware = now

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date < now_aware:
            raise forms.ValidationError(
                'Start date %(start)s must be greater than current time %(now)s',
                params={
                    'start': start_date,
                    'now': now_aware
                },
            )
        if start_date >= end_date:
            raise forms.ValidationError('Start date must be less than the End date.')


class ContestUpdateForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.HiddenInput())
    url = forms.CharField()
    image = forms.FileField(required=False)
    start_date = forms.DateField(
        help_text="Please use the following format: YYYY-MM-DD HH:MM:ss. e.g, 2018-08-14 22:10:24."
    )
    end_date = forms.DateField()
    award_description = forms.CharField(max_length=200)

    def clean(self):
        cleaned_data = super().clean()

        """Validate start date."""
        now = datetime.date.today()

        # Now datetime is naive, so it is localized
        # to the current user timezone.
        #now_aware = pytz.utc.localize(now)
        now_aware = now

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date < now_aware:
            raise forms.ValidationError(
                'Start date %(start)s must be greater than current time %(now)s',
                params={
                    'start': start_date,
                    'now': now_aware
                },
            )
        if start_date >= end_date:
            raise forms.ValidationError('Start date must be less than the End date.')


class VideoForm(forms.Form):
    # contest_name = forms.CharField(max_length=200, widget=forms.HiddenInput(),required=False)
    video = forms.FileField()
    participant_fname = forms.CharField(label='Nombre del Participante',max_length=200)
    participant_lname = forms.CharField(label='Apellido del Participante',max_length=200)
    participant_email = forms.EmailField(label='Correo del Participante')
    # upload_at = forms.DateField(auto_now_add=True)
    description = forms.CharField(label='Descripción del Video',max_length=600)
    # status = forms.CharField(max_length=20)
    # S3 image url
    s3_video_url = forms.CharField(max_length=200, widget=forms.HiddenInput(),required=False)