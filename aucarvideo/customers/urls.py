# -- encoding: utf-8 --

from django.urls import path

from customers.views import ClientCreate


urlpatterns = [
    path('create/', ClientCreate.as_view(), name='create'),
]