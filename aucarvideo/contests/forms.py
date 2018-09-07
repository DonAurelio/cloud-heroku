from django.forms import ModelForm
from contests.models import Video
from contests.models import Participant


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['file','description']


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name','last_name','email']