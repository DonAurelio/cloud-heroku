from django.db import models
from django.core.mail import send_mail


class Contest(models.Model):

    # The conetxt unique URL
    url = models.CharField(max_length=200,blank=True,null=True,unique=True)
    # The name of the competition
    name = models.CharField(max_length=100,blank=False,null=False,unique=True)
    # The banner image of the contests
    banner = models.ImageField(upload_to='contests/banner',blank=True,null=False)
    # The date on which te contests start
    start_date = models.DateField(blank=False,null=False)
    # The date on which the contests ends
    end_date = models.DateField(blank=False,null=False)
    # Description of the award
    award_description = models.TextField(blank=False,null=False)

    def __str__(self):
        return self.name.title()


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

    def __str__(self):
        return self.email


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
    # The contests to which the video belongs
    contest = models.ForeignKey(Contest,on_delete=models.CASCADE,blank=True,null=True)
    # The participant who uploaded the video
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    # The date on which the video was uploaded
    uploaded_at = models.DateField(auto_now_add=True)
    # The status of the video convertion.
    status = models.CharField(max_length=20,choices=STATUS,default=PROCESSING)

    class Meta:
        # Ordering by descending order
        ordering = ['-uploaded_at']

    def was_processed(self):
        """
        If the uploaded video has .mp4 it does not
        need to be converted. So it was not converted.
        """
        return '.mp4' in file.url

    def get_converted_url(self):
        # File name without extension
        file_name = self.file.url[:-4]
        # The name of the file that should be assigned to the 
        # converted file
        return f'{file_name}_{self.CONVERTED}.mp4'


#     def notify_video_publication(self):
#         send_mail(
#             subject=self.participant.email, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )
        
#     def _notify_video_processing(self):
#         pass

