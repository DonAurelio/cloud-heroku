# -- encoding: utf-8 --

from django.urls import path

from customers.views import ClientCreate
from customers.views import ClientListJson


urlpatterns = [
    path('create/', ClientCreate.as_view(), name='create'),
    path('api/client/list/', ClientListJson.as_view(), name='client_list_json'),
]