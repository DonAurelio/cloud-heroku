from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.http import JsonResponse

from customers.forms import ClientForm
from customers.models import Client


class ClientCreate(TemplateView):

    def get(self, request,*args,**kwargs):
        client_form = ClientForm()
        template_name = 'customers/client_form.html'
        context = {
            'client_form': client_form,
            
        }
        return render(request,template_name,context)

    def post(self, request,*args,**kwargs):
        client_form = ClientForm(request.POST)

        if client_form.is_valid() :
            client = client_form.save(commit=False)
            client.domain_url = client.name + '.' + settings.DOMAIN_NAME
            client.schema_name = client.name
            client.save()
           
            return redirect('http://'+client.domain_url+':8000/auth_tenants/register')
            
        else:
            template_name = 'customers/client_form.html'
            context = {
                'client_form': client_form,
            }

            return render(request,template_name,context)


class ClientListJson(TemplateView):

    def get(self,request,*args,**kwargs):
        clients = Client.objects.all().exclude(schema_name='public')
        clients = [ client.domain_url for client in clients ]

        return JsonResponse(data=clients,safe=False)