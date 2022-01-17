from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
# from authoring.models import Story, StoryOwner



# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	# following = models.ManyToManyField('self', blank=True, related_name='following', symmetrical=False)
	# image
	# location
	# bio

	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

	def __str__(self):
		return '%s' % (self.user.username)

class ProfileConnection(models.Model):
	profile = models.ForeignKey(Profile, related_name='profile', on_delete=models.CASCADE)
	contact = models.ForeignKey(Profile, related_name='contact', on_delete=models.CASCADE)
	verified = models.BooleanField(default=False)

	# @receiver(post_save, sender=ProfileConnection)
	# def create_second_connection(sender, instance, created, **kwargs):
	# 	if created:
	# 		print('CREATED: ', sender, instance, created, kwargs)
	# 		# ProfileConnection.objects.create()

	def __str__(self):
		# connection['connection'] = '%s-%s' % (self.profile, self.contact)
		# connection['profile'] = '%s' % (self.profile)
		connection = '%s' % (self.contact)
		return connection

	class Meta:
		unique_together = (('profile', 'contact'))