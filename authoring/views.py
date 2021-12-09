from django.utils.text import slugify
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, reverse

from .forms import StoryForm

from .models import Story, StoryPage, StoryPath
from userprofile.models import Profile
# Create your views here.

class StoryIndexView(ListView):
	model = Story
	template_name = 'authoring/story_list.html'

class StoryCreateView(CreateView):
	model = Story
	form_class = StoryForm
	# fields = '__all__'
	template_name = 'authoring/story_create_form.html'

	def post(self, request):
		if request.method=='POST':
			form = StoryForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new_story = form.save(commit=False)
			new_story.started_by = Profile.objects.get(user=request.user)
			new_story.slug = slugify(new_story.title)
			new_story.save()
		return redirect(reverse('author:story_detail', kwargs={'storyslug':new_story.slug}))

class StoryDetailView(DetailView):
	model = Story
	template_name = 'authoring/story_detail.html'
	fields = ['title', 'started_by']
	slug_url_kwarg = 'storyslug'