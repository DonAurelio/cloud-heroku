# -- encoding: utf-8 --

from django.urls import path

from profile.views import RegisterView
from profile.views import LoginView
from profile.views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]