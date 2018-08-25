# -- encoding: utf-8 --

from django.urls import path

from thome.views import Thome

urlpatterns = [
    path('thome/', Thome.as_view(), name='thome'),
]