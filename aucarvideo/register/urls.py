# -- encoding: utf-8 --

from django.urls import path

from register.views import SignUpView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
]