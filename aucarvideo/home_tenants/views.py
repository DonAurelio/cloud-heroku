from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class Index(TemplateView):
    def get(self, request,*args,**kwargs):

        if request.user.is_authenticated:
            return redirect('contests:list_admin')

        return redirect('contests:list')
