from django.db import models
from cms.models import CMSPlugin
from authoring.models import Story

# Create your models here.
class StoryPluginModel(CMSPlugin):
	story = models.ForeignKey(Story, on_delete=models.CASCADE)

	def __str__(self):
		return self.story.title