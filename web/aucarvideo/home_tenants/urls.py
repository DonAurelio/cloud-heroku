from django.urls import path
from django.urls import reverse_lazy

from home_tenants.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
]