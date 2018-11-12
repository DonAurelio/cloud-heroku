from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import views
from django.db import transaction

from perfiles.forms import UserCreateForm
from perfiles.models import DynamoCompanyManager


class RegisterView(TemplateView):
    def get(self, request,*args,**kwargs):
        user_form = UserCreateForm()
        template_name = 'perfiles/register_form.html'
        context = {
            'user_form': user_form
        }
        return render(request,template_name,context)

    def post(self, request,*args,**kwargs):
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            
            # If some error occurs the database is rolled back
            with transaction.atomic():
                new_user = user_form.save()
                manager = DynamoCompanyManager()
                manager.create_company(company_name=new_user.company_name)
            
            return redirect('perfiles:login')
            

        template_name = 'perfiles/register_form.html'
        context = {
            'user_form': user_form,
        }

        return render(request,template_name,context)



class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        login_form = AuthenticationForm()
        template_name = 'perfiles/login.html'
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
                login(request, user)
                return redirect('contests:contest_admin_list')
        else:
            template_name = 'perfiles/login.html'
            context = {
                'login_form': login_form
            }
            return render(request, template_name, context)


class LogoutView(views.LogoutView):
    """Deals with user logout process."""

    # The URL to redirect to after logout. Defaults to settings.LOGOUT_REDIRECT_URL.
    next_page = '/'