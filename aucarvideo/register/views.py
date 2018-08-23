from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from register.forms import ClientForm
from django.contrib.auth.forms import UserCreationForm

class SignUpView(TemplateView):
    def get(self, request,*args,**kwargs):
        client_form = ClientForm()
        user_form = UserCreationForm()
        template_name = 'register/login.html'
        context = {
            'client_form': client_form,
            'user_form': user_form
        }
        return render(request,template_name,context)

    def post(self, request,*args,**kwargs):
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client_form.save()
            
            return HttpResponse('exiiitooo')
        else:
            template_name = 'register/login.html'
            context = {
                'client_form': client_form,
            }

            return render(request,template_name,context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context