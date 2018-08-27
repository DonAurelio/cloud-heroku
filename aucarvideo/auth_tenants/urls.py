# -- encoding: utf-8 --

from django.urls import path

from auth_tenants.views import RegisterView
from auth_tenants.views import LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]