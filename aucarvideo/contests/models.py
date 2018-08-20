from django.db import models


class VideoContest(models.Model):


    # The name of the competition
    name = models.CharField(max_length=100,blank=True,null=True)
    # The banner image of the contest
    banner =  models.ImageField(upload_to='contests/banner',blank=True,null=True)
    # The conetxt unique URL
    url = models.URLField(max_length=200, blank=True,null=True)
    # The date on which te contest start
    start_date = models.DateField(blank=True,null=True)
    # The date on which the contest ends
    end_date = models.DateField(blank=True,null=True)
    # Description of the award
    award_description = models.TextField(blank=True,null=True)


class Participant(models.Model):
    """
    A Participant is a persona that upload a video
    for a given Video Contest.
    """

    # The first name of the person who upload the video
    first_name = models.CharField(max_length=100,blank=True,null=True)
    # The last name of the person who upload the video
    last_name = models.CharField(max_length=100,blank=True,null=True)
    # The email of the person who upload the video
    email = models.EmailField(max_length=100,blank=True,null=True)



class Video(models.Model):
    """
    A video represents a video that a participant
    upload to a given Video Context.
    """

    PROCESSING = 'Processing'
    CONVERTED = 'Converted'

    STATUS = (
        (PROCESSING, 'Processing'),
        (CONVERTED, 'Converted'),
    )

    # The proper video uploaded by the participant
    file = models.FileField(upload_to='contests/videos')
    # The contest to which the video belongs
    contest = models.ForeignKey(VideoContest,on_delete=models.CASCADE)
    # The participant who uploaded the video
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    # The date on which the video was uploaded
    uploaded_at = models.DateField(auto_now_add=True)
    # The status of the video convertion.
    status = models.CharField(max_length=20,choices=STATUS,default=PROCESSING)







