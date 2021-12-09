from django.conf import settings
from django.db import models
from userprofile.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
# from django_currentuser.middleware import get_current_authenticated_user
    

# Create your models here.
class Story(models.Model):
	title = models.CharField(max_length=250, null=True, blank=True)
	subtitle = models.CharField(max_length=250, null=True, blank=True)
	synopsis = models.TextField(max_length=500, null=True, blank=True)
	authors = models.ManyToManyField(Profile, through='StoryOwner')
	started_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='started_by', verbose_name='Started by')
	slug = models.SlugField(null=True, blank=True)

	class Meta:
		verbose_name = 'Story'
		verbose_name_plural = 'Stories'

	def __str__(self):
		return '%s' % (self.title)

	def get_absolute_url(self):
		return reverse('story', kwargs={'slug':self.slug})

	def save(self, *args, **kwargs):
		self.slug = self.slug or slugify(self.title)
		super(Story, self).save(*args, **kwargs)

class StoryOwner(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)

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
			StoryOwner.objects.create(story=instance, user=user)


class StoryPage(models.Model):
	title = models.CharField(max_length=250, null=True, blank=True)
	story = models.ForeignKey('Story', on_delete=models.CASCADE)
	challenge = models.BooleanField(default=False, null=True, blank=True)
	start = models.BooleanField(default=False, null=True, blank=True)
	end = models.BooleanField(default=False, null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)

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

