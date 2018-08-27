# -- encoding: utf-8 --

from django.urls import path
from django.conf.urls import url

from contests.views import ContestCreate
from contests.views import ContestList
from contests.views import ContestUpdate
from contests.views import ContestAdminList
from contests.views import ContestDelete
from contests.views import VideoAdminList


urlpatterns = [
    path('contest/create/', ContestCreate.as_view(), name='contest_create'),
    path('contest/<int:pk>/delete/',ContestDelete.as_view(),name='contest_delete'),
    path('contest/<str:url>/update/',ContestUpdate.as_view(),name='contest_update'),
    path('contest/list/',ContestList.as_view(),name='contest_list'),

    path('admin/contest/list/',ContestAdminList.as_view(),name='contest_admin_list'),
    path('admin/video/<str:url>/',VideoAdminList.as_view(),name='video_admin_list'),
    # path('contest/<int:url>/video/list/',VideoAdminList.as_view(),name='video_admin_list'),


]

