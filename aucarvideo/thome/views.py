from django.shortcuts import render
from django.views.generic.base import TemplateView
from contests.models import VideoContest


class Thome(TemplateView):
    def get(self, request,*args,**kwargs):
        concursos = list()
        concursos = VideoContest.objects.all()

        concursos_ordenados = sorted(concursos, key=lambda x: x.start_date, reverse=True)
        return render(request, 'thome/thome.html', {
            'concursos_ordenados': concursos_ordenados
        })