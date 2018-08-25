# -- encoding: utf-8 --

from django.urls import path

from contests.views import NewContest

urlpatterns = [
    path('videocontest_form/', NewContest.as_view(), name='videocontest_form'),
]