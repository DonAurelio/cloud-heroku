# -- encoding: utf-8 --

from django.urls import path

from auth_tenants.views import RegisterView
from auth_tenants.views import LoginView
from auth_tenants.views import LogoutView

urlpatterns = [
    path('auth_tenants/register/', RegisterView.as_view(), name='register'),
    path('auth_tenants/login/', LoginView.as_view(), name='login'),
    path('auth_tenants/logout/', LogoutView.as_view(), name='logout'),
]