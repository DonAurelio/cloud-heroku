from django.shortcuts import render, redirect, reverse
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
        user_form = UserCreationForm(request.POST)
        if client_form.is_valid() and user_form.is_valid():

            url = client_form.cleaned_data ["domain_url"]
            client_form2 = client_form.save(commit=False)
            domine = url
            client_form2.domain_url = domine + ".localhost"

            # print(client_form.cleaned_data) 
            # print(url)
            client_form2.save()
            user_form.save()



            # domain_url = client_form.URLField(queryset=..., to_field_name="domain_url")
            # client_form.save()

           
            return redirect('http://'+client_form2.domain_url+':8000/login/login')
            
        else:
            template_name = 'register/login.html'
            context = {
                'client_form': client_form,
                'user_form': user_form,
            }

            return render(request,template_name,context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context