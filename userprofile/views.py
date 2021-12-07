from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Profile

# Create your views here.
class ProfileBaseView(LoginRequiredMixin):
	model = Profile 
	# Users = get_user_model()

	def get_object(self):
		user = Profile.objects.get(user=get_user_model().objects.get(username=self.kwargs.get('username')))
		print(user)
		return 
		

class ProfileDetailView(ProfileBaseView, DetailView):
	template_name = 'userprofile/profile_detail.html'

class ProfileCreateView(ProfileBaseView, CreateView):
	template_name = 'userprofile/profile_form.html'

class ProfileUpdateView(ProfileBaseView, UpdateView):
	template_name = 'userprofile/profile_form.html'