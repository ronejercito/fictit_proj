from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render

from .models import Story, StoryPage, StoryPath
# Create your views here.

class StoryIndexView(ListView):
	model = Story
	template_name = 'authoring/story_list.html'

class StoryCreateView(CreateView):
	model = Story
	fields = '__all__'
	template_name = 'authoring/story_create_form.html'

class StoryDetailView(DetailView):
	model = Story
	template_name = 'authoring/story_detail.html'