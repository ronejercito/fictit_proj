from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Profile, ProfileConnection
from .forms import ProfileConnectionForm, SearchUserForm

# Create your views here.
class ProfileBaseView(LoginRequiredMixin):
	model = Profile 

	def get_object(self):
		user = Profile.objects.get(user=get_user_model().objects.get(username=self.kwargs.get('username')))
		return user
		

class ProfileDetailView(ProfileBaseView, DetailView):
	template_name = 'userprofile/profile_detail.html'

	def get_context_data(self, **kwargs):
		'''Checks if a connection between user and object profile have a connection (friends). If connected, send EXISTS to template. Template will not render CONNECT BUTTON'''
		context = super(ProfileDetailView, self).get_context_data(**kwargs)
		user = get_user_model().objects.get(username=self.kwargs['username'])
		profile = Profile.objects.get(user=self.request.user)
		contact = Profile.objects.get(user=user)
		try:
			context['exists'] = ProfileConnection.objects.filter(profile=profile).filter(contact=contact).exists()
		except Exception as e:
			context['exists'] = False
		return context

# class ProfileCreateView(ProfileBaseView, CreateView):
# 	template_name = 'userprofile/profile_form.html'

class ProfileUpdateView(ProfileBaseView, UpdateView):
	template_name = 'userprofile/profile_form.html'

class MyGroupListView(LoginRequiredMixin, ListView):
	template_name = 'userprofile/group_list.html'
	model = ProfileConnection

	def get_queryset(self, **kwargs):
		query = self.request.GET.get('q')
		profile = Profile.objects.get(user=get_user_model().objects.get(username=self.request.user))
		object_list = self.model.objects.filter(profile=profile) # NEEDS SEARCH SIMILAR TO WORD OR STARTS WITH; See: https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects
		return object_list 

	def get_context_data(self, storyslug=None, **kwargs):
	    context = super(MyGroupListView, self).get_context_data(**kwargs)
	    if 'storyslug' in self.kwargs:
	    	context['story']=self.kwargs['storyslug']
	    return context

class SearchUserView(TemplateView):
	template_name = 'userprofile/profilesearch_form.html'


# PROFILE CONNECTIONS
class ProfileConnectionBaseView(LoginRequiredMixin):
	model = ProfileConnection

class ProfileConnectionListView(ProfileConnectionBaseView, ListView):
	template_name = 'userprofile/profileconnection_list.html'

	def get_context_data(self, **kwargs):
		'''Returns only connections of user'''
		context = super(ProfileConnectionBaseView, self).get_context_data(**kwargs)
		profile = Profile.objects.get(user=self.request.user)
		context['connections'] = self.model.objects.filter(profile=profile).filter(verified=True)
		return context

class ProfileConnectionCreateView(ProfileConnectionBaseView, CreateView):
	form_class = ProfileConnectionForm
	username = ''

	def get(self, request, **kwargs):
		self.username = self.kwargs['username']
		contact = get_user_model().objects.get(username=self.username)
		profile = Profile.objects.get(user=self.request.user)
		initial = {'profile':profile, 'contact': contact, 'verified':False}
		form = self.form_class(initial=initial)
		return render(request, 'userprofile/profileconnection_form.html', {'form':form, 'contact':self.username})

	def get_success_url(self):
		'''Returns user to the profile they were viewing'''
		return reverse('profile:profile_detail', kwargs={'username':self.request.user})

class ProfileConnectionDeleteView(ProfileConnectionBaseView, DeleteView):
	template_name = 'userprofile/profileconnection_delete.html'