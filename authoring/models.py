from django.conf import settings
from django.db import models
from userprofile.models import Profile

# Create your models here.
class Story(models.Model):
	title = models.CharField(max_length=250, null=True, blank=True)
	authors = models.ManyToManyField(Profile, through='StoryOwner')

	def __str__(self):
		return '%s' % (self.title)

	class Meta:
		verbose_name = 'Story'
		verbose_name_plural = 'Stories'

class StoryOwner(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)

	def __str__(self):
		return '%s-%s' % (self.story.title, str(self.user))

class StoryPage(models.Model):
	title = models.CharField(max_length=250, null=True, blank=True)
	story = models.ForeignKey('Story', on_delete=models.CASCADE)
	challenge = models.BooleanField(default=False, null=True, blank=True)
	start = models.BooleanField(default=False, null=True, blank=True)
	end = models.BooleanField(default=False, null=True, blank=True)

	def __str__(self):
		return '%s' % (self.title)

	class Meta:
		verbose_name = 'Story Page'
		verbose_name_plural = 'Story Pages'

class StoryPath(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story', null=True, blank=True)
	storypage = models.ForeignKey(StoryPage, on_delete=models.CASCADE, related_name='story_page')
	storypath = models.ForeignKey(StoryPage, on_delete=models.SET_NULL, related_name='story_path', null=True, blank=True)
	correct = models.BooleanField(default=False, null=True, blank=True)

	class Meta:
		unique_together=['story', 'storypage', 'storypath']

	def __str__(self):
		return '%s-%s-%s' % (self.story.title, self.storypage.title, self.storypath.title)

