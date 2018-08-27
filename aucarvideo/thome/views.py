from django.shortcuts import render, redirect, reverse
from django.views.generic.base import TemplateView
from contests.models import VideoContest
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm




class Thome(TemplateView):
    def get(self, request,*args,**kwargs):
        concursos = list()
        concursos = VideoContest.objects.all()

        concursos_ordenados = sorted(concursos, key=lambda x: x.start_date, reverse=True)
        return render(request, 'thome/thome.html', {
            'concursos_ordenados': concursos_ordenados
        })


class RegisterView(TemplateView):
    def get(self, request,*args,**kwargs):
        user_form = UserCreationForm()
        template_name = 'thome/register_adm.html'
        context = {
            'user_form': user_form
        }
        return render(request,template_name,context)

    def post(self, request,*args,**kwargs):
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
           
            return redirect('thome:thome')
            
        else:
            template_name = 'thome/register_adm.html'
            context = {
                'user_form': user_form,
            }

            return render(request,template_name,context)
