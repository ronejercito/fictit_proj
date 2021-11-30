from django.db import models
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool

# Create your models here.
class Story(PageExtension):
	def __str__(self):
		return '%s' % (self.title)

	class Meta:
		verbose_name = 'Story'
		verbose_name_plural = 'Stories'

# class StoryOwner(models.Model):
# 	pass
# 	# user

class StoryPage(PageExtension):
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
	storypage = models.ForeignKey('StoryPage', on_delete=models.CASCADE, related_name='story_page')
	storypath = models.ForeignKey('StoryPage', on_delete=models.SET_NULL, related_name='story_path', null=True, blank=True)
	correct = models.BooleanField(default=False, null=True, blank=True)