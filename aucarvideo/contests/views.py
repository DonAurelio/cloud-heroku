from django.views.generic.edit import CreateView
from contests.models import VideoContest

class NewContest(CreateView):
    model = VideoContest
    fields = ['name','banner','url','url','start_date','end_date','award_description']

