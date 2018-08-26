from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from contests.models import VideoContest
from django.shortcuts import render, redirect, reverse

class NewContest(CreateView):
    model = VideoContest
    fields = ['name','banner','url','url','start_date','end_date','award_description']

    def get_success_url(self):
        return reverse('thome:thome')


class ContestDelete(DeleteView):
    model = VideoContest
    success_url = reverse_lazy('thome:thome')



