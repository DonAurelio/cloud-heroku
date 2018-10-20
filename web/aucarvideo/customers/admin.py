from django.contrib import admin
from customers.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_on')
    search_fields = ('name',)
