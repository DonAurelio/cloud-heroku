# -- encoding: utf-8 --

from django.urls import path

from perfiles.views import RegisterView
from perfiles.views import LoginView
from perfiles.views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]