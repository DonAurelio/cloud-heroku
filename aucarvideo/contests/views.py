from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.shortcuts import reverse, render
from django.urls import reverse_lazy

from contests.models import Contest


class ContestCreate(CreateView):
    model = Contest
    template_name = 'contests/contest_form.html'
    fields = [
        'name','banner','url','url','start_date',
        'end_date','award_description'
    ]

    def get_success_url(self):
        return reverse('contests:list')


class ContestList(ListView):
    model = Contest
    template_name = 'contests/contest_list.html'


class ContestDelete(DeleteView):
    model = Contest
    success_url = reverse_lazy('contests:list')


class ContestListAdmin(TemplateView):

    def get(self, request,*args,**kwargs):
        concursos = list()
        concursos = Contest.objects.all()

        concursos_ordenados = sorted(concursos, key=lambda x: x.start_date, reverse=True)
        return render(request, 'contests/contest_admin_list.html', {
            'concursos_ordenados': concursos_ordenados
        })


