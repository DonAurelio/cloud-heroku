from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate


class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        login_form = AuthenticationForm()
        template_name = 'login/login.html'
        context = {
            'login_form': login_form
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        login_form = AuthenticationForm(request=request, data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return HttpResponse('exiiitooo')
        else:
            template_name = 'login/login.html'
            context = {
                'login_form': login_form
            }
            return render(request, template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context