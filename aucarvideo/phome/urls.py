# -- encoding: utf-8 --

from django.urls import path

from phome.views import Home


urlpatterns = [
    path('', Home.as_view(), name='home'),

]