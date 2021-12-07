from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
# from authoring.models import Story, StoryOwner



# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

	def __str__(self):
		return self.user.username