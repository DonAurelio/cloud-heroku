from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from contests.models import VideoContest, Video
from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView

class NewContest(CreateView):
    model = VideoContest
    fields = ['name','banner','url','url','start_date','end_date','award_description']

    def get_success_url(self):
        return reverse('thome:thome')


class ContestDelete(DeleteView):
    model = VideoContest
    success_url = reverse_lazy('thome:thome')


class ContestUpdate(UpdateView):
    model = VideoContest
    fields = ['name','banner','url','url','start_date','end_date','award_description']

    def get_success_url(self):
        return reverse('thome:thome')



class VideoList(TemplateView):
    def get(self, request, contest_id):
        videos = Video.objects.filter(contest_id=contest_id)
        return render(request, 'contests/video_list.html', {'videos': videos})
