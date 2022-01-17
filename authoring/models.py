from django.conf import settings
from django.db import models
from userprofile.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Story(models.Model):
	title = models.CharField(max_length=250, null=True, blank=True)
	subtitle = models.CharField(max_length=250, null=True, blank=True)
	synopsis = models.TextField(max_length=500, null=True, blank=True)
	authors = models.ManyToManyField(Profile, through='StoryOwner')
	started_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='started_by', verbose_name='Started by')
	slug = models.SlugField(null=True, blank=True)
	publish = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Story'
		verbose_name_plural = 'Stories'

	def __str__(self):
		return '%s' % (self.title)

	def get_absolute_url(self):
		return reverse('author:story_detail', kwargs={'storyslug':self.slug})

	def save(self, *args, **kwargs):
		self.slug = self.slug or slugify(self.title)
		super(Story, self).save(*args, **kwargs)

class StoryOwner(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	role = models.CharField(max_length=100, null=True, blank=True)

	class Meta:
		unique_together = ['story', 'user']
		verbose_name = 'Story Owner'
		verbose_name_plural = 'Story Owners'

	def __str__(self):
		return '%s-%s' % (self.story.title, str(self.user))

	@receiver(post_save, sender=Story)
	def add_author(sender, instance, created, **kwargs):
		if created:
			user = instance.started_by
			StoryOwner.objects.create(story=instance, user=user, role='Creator')


class StoryPage(models.Model):
	title = models.CharField(max_length=250, null=True, blank=True)
	text = models.TextField(max_length=5000, null=True, blank=True)
	story = models.ForeignKey('Story', on_delete=models.CASCADE)
	challenge = models.BooleanField(default=False)
	start = models.BooleanField(default=False)
	end = models.BooleanField(default=False)
	slug = models.SlugField(null=True, blank=True)
	publish = models.BooleanField(default=False)

	def __str__(self):
		return '%s' % (self.title)

	class Meta:
		verbose_name = 'Story Page'
		verbose_name_plural = 'Story Pages'

class StoryPath(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story', null=True, blank=True)
	storypage = models.ForeignKey(StoryPage, on_delete=models.CASCADE, related_name='story_page')
	storypath = models.ForeignKey(StoryPage, on_delete=models.CASCADE, related_name='story_path')
	correct = models.BooleanField(default=False, null=True, blank=True)

	class Meta:
		unique_together=['story', 'storypage', 'storypath']

	def __str__(self):
		return '%s:[%s]-[%s]' % (self.story.title, self.storypage.title, self.storypath.title)

class BaseComment(models.Model):
	commenter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	text = models.TextField(max_length=500, null=True)
	resolved = models.BooleanField(default=False)
	resolve_date = models.DateTimeField(null=True, blank=True)

	class Meta:
		abstract = True

class Comment(BaseComment):
	page = models.ForeignKey(StoryPage, on_delete=models.CASCADE)
	quote = models.TextField(max_length=100, null=True, blank=True)
	start_point = models.PositiveIntegerField(null=True, blank=True)
	length = models.PositiveIntegerField(null=True, blank=True) # LENGTH OF QUOTED TEXT

	class Meta:
		ordering = ['updated']

	def __str__(self):
		return f'Comment by {self.commenter.user} on {self.page} [{self.updated}]'

class Response(BaseComment):
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

	class Meta:
		ordering = ['updated']

	def __str__(self):
		return f'Response by {self.commenter.user} on {self.comment} [{self.updated}]'
