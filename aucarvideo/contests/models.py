from django.db import models


class VideoContest(models.Model):

	# The name of the competition
	name = models.CharField(max_length=100,blank=True,null=True)
