# -- encoding: utf-8 --

from django.urls import path
from django.conf.urls import url


from contests.views import (
    NewContest,
    ContestDelete)

urlpatterns = [
    path('videocontest_form/', NewContest.as_view(), name='videocontest_form'),
    url(r'^videocontest_confirm_delete/(?P<pk>\d+)$',ContestDelete.as_view(),name='videocontest_confirm_delete'),
]