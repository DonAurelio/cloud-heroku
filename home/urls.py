# -- encoding: utf-8 --

from django.urls import path

from home.views import Index


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('index/', Index.as_view(), name='index'),
]