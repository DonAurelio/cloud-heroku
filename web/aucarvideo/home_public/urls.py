# -- encoding: utf-8 --

from django.urls import path

from home_public.views import Index


urlpatterns = [
    path('', Index.as_view(), name='index'),
]