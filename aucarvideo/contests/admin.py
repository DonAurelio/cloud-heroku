from django.contrib import admin

from contests.models import Contest
from contests.models import Participant
from contests.models import Video


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('id','name','url','start_date','end_date','award_description')
    search_fields = ('name',)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','last_name')
    search_fields = ('first_name','last_name','last_name')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','file','contest','participant','uploaded_at','status')
    search_fields = ('file','contests')