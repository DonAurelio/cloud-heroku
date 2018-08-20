from django.contrib import admin
from customers.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','name','schema_name','domain_url','created_on')
    search_fields = ('schema_name','name')
