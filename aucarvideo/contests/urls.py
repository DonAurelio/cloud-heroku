# -- encoding: utf-8 --

from django.urls import path
from django.conf.urls import url


from contests.views import (
    NewContest,
    ContestDelete,
    ContestUpdate,
    VideoList)

urlpatterns = [
    url(r'^videocontest_form$', NewContest.as_view(), name='videocontest_form'),
    url(r'^editarContest/(?P<pk>\d+)$', ContestUpdate.as_view(), name='editContest'),
    url(r'^videocontest_confirm_delete/(?P<pk>\d+)$',ContestDelete.as_view(),name='videocontest_confirm_delete'),
    url(r'^video_list/(?P<contest_id>\d+)$', VideoList.as_view(), name='video_list')

]