# -- encoding: utf-8 --

from django.urls import path
from django.conf.urls import url

from contests.views import ContestCreate
from contests.views import ContestList
from contests.views import ContestListAdmin
from contests.views import ContestDelete


urlpatterns = [
    path('create/', ContestCreate.as_view(), name='create'),
    path('delete/<int:pk>/',ContestDelete.as_view(),name='delete'),
    path('list/',ContestList.as_view(),name='list'),

    path('list_admin/',ContestListAdmin.as_view(),name='list_admin'),
]
