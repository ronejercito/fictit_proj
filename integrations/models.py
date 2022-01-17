from django.db import models
from cms.models import CMSPlugin
from authoring.models import Story, StoryOwner, StoryPage

# Create your models here.
class StoryPluginModel(CMSPlugin):
	story = models.ForeignKey(Story, on_delete=models.CASCADE)

	def __str__(self):
		return self.story.title

class StoryOwnerPluginModel(CMSPlugin):
	storyowner = models.ForeignKey(StoryOwner, on_delete=models.CASCADE)

	def __str__(self):
		return self.storyowner

class StoryPagePluginModel(CMSPlugin):
	storypage =models.ForeignKey(StoryPage, on_delete=models.CASCADE)

	def __str__(self):
		return self.storypage.title