# -- encoding: utf-8 --

from django.urls import path

from register.views import RegisterView
from register.views import LoginView
from register.views import LogoutView

urlpatterns = [
    path('register/<int:pk>/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]