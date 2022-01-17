from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.text import slugify
from django.views.generic import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse

from .forms import StoryForm, StoryPageForm, StoryPathForm, CommentForm

from .models import Story, StoryPage, StoryPath, StoryOwner, StoryPage, StoryPath, Comment
from userprofile.models import Profile
# Create your views here.

# STORY
class StoryBaseView(LoginRequiredMixin):
	model = Story

class StoryIndexView(StoryBaseView, ListView):
	template_name = 'authoring/story_list.html'

class StoryCreateView(StoryBaseView, CreateView):
	form_class = StoryForm
	template_name = 'authoring/story_form.html'

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

class StoryDetailView(StoryBaseView, DetailView):
	template_name = 'authoring/story_detail.html'
	form_class = StoryForm
	slug_url_kwarg = 'storyslug'

	def get_context_data(self, **kwargs):
		context = super(StoryDetailView, self).get_context_data(**kwargs)
		context['storyowners'] = StoryOwner.objects.filter(story=self.object)
		context['storypages'] = StoryPage.objects.filter(story=self.object)
		return context

class StoryDeleteView(StoryBaseView, DeleteView):
	template_name = 'authoring/story_confirm_delete.html'
	success_url = 'author:story_index'


# STORYOWNER
class StoryOwnerBaseView(LoginRequiredMixin):
	model = StoryOwner

class StoryOwnerCreator(StoryOwnerBaseView, View):

	def post(self, request, **kwargs):
		if request.method =='POST':
			# Check if valid user (Story Creator)
			story = Story.objects.get(slug=self.kwargs.get('storyslug')) # GET THE STORY
			creator = Profile.objects.get(user=self.request.user)# GET THE USER WHO STARTED THE STORY
			user = get_user_model().objects.get(username=self.kwargs['username'])
			new_author = Profile.objects.get(user=user)

			if creator == story.started_by: # CHECK IF THE CURRENTLY LOGGED IN USER IS THE SAME AS THE CREATOR
				# Create StoryOwner
				StoryOwner(story=story, user=new_author).save()
				messages.success(request, 'New author added')
			else:
				messages.error(request, 'You are not authorized to add this author.')
		return redirect(reverse('author:story_detail', kwargs={'storyslug':self.kwargs.get('storyslug')}))

class StoryOwnerDeleteView(StoryOwnerBaseView, View):
	
	def post(self, request, **kwargs):
		if request.method =='POST':
			# Check if valid user (Story Creator)
			story = Story.objects.get(slug=self.kwargs.get('storyslug')) # GET THE STORY
			creator = Profile.objects.get(user=self.request.user)# GET THE USER WHO STARTED THE STORY

			if creator == story.started_by: # CHECK IF THE CURRENTLY LOGGED IN USER IS THE SAME AS THE CREATOR
				# Create StoryOwner
				StoryOwner.objects.get(id=self.kwargs['pk']).delete()
				messages.success(request, 'Author removed')
			else:
				messages.error(request, 'You are not authorized to remove this author.')
		return redirect(reverse('author:story_detail', kwargs={'storyslug':self.kwargs.get('storyslug')}))



# STORYPAGES
class StoryPageBase(LoginRequiredMixin):
	model = StoryPage
	slug_url_kwarg = 'storyslug'

class StoryPageCreateView(StoryPageBase, CreateView): # NEED TO VERIFY IF USER IS AN AUTHOR
	template_name = 'authoring/storypage/storypage_form.html'
	form_class = StoryPageForm

	def post(self, request, **kwargs):
		if request.method=='POST':
			form = StoryPageForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new_storypage = form.save(commit=False)
			new_storypage.story = Story.objects.get(slug=self.kwargs.get('storyslug'))
			new_storypage.slug = slugify(new_storypage.title)
			new_storypage.save()
		return redirect(reverse('author:storypage_update', kwargs={'storyslug':self.kwargs.get('storyslug'), 'storypageslug':new_storypage.slug}))

class StoryPageDetailView(StoryPageBase, DetailView):
	template_name = 'authoring/storypage/storypage_detail.html'
	slug_url_kwarg = 'storypageslug'
	fields = ['title', 'text', 'challenge', 'start', 'end', 'publish']

class StoryPageUpdateView(StoryPageBase, UpdateView):
	template_name = 'authoring/storypage/storypage_form.html'
	slug_url_kwarg = 'storypageslug'
	form_class = StoryPageForm 

	def get_context_data(self, **kwargs):
	    context = super(StoryPageUpdateView, self).get_context_data(**kwargs)
	    story = Story.objects.get(slug=self.kwargs.get('storyslug'))
	    addpath_form = StoryPathForm(self.kwargs.get('storyslug'), self.kwargs.get('storypageslug'))
	    addcomment_form = CommentForm(None)
	    comments = Comment.objects.filter(story=story, page=self.object)
	    try:
	    	context['paths'] = StoryPath.objects.filter(story=story, storypage=self.object)
	    	context['addpath_form'] = addpath_form
	    	context['addcomment_form'] = addcomment_form
	    	if comments:
	    		context['comments'] = comments
	    except:
	    	pass
	    return context

	def get_success_url(self):
		messages.success(self.request, 'Page updated.')
		return reverse('author:story_detail', kwargs={'storyslug':self.kwargs.get('storyslug')})


class StoryPageDeleteView(StoryPageBase, DeleteView):
	template_name = 'authoring/storypage/storypage_confirm_delete.html'
	slug_url_kwarg = 'storypageslug'

	def get_success_url(self):
		messages.success(self.request, 'Page removed.')
		return reverse('author:story_detail', kwargs={'storyslug':self.kwargs.get('storyslug')})


# STORYPATH
class StoryPathBase(LoginRequiredMixin):
	model = StoryPath

class StoryPathCreateView(StoryPathBase, CreateView):
	template_name = StoryPathForm
	fields = ['storypath', 'correct']

	def post(self, request, **kwargs):
		if request.method == 'POST':
			form = self.get_form()

		if form.is_valid():
			cd = form.cleaned_data
			new_path = form.save(commit=False)
			new_path.story = Story.objects.get(slug=self.kwargs.get('storyslug'))
			new_path.storypage = StoryPage.objects.get(slug=self.kwargs.get('storypageslug'))

			user = Profile.objects.get(user=self.request.user)
			storyowner_list = StoryOwner.objects.filter(story=new_path.story).values('user')
			authors = []

			for a in storyowner_list:
				author = Profile.objects.get(user=a['user'])
				authors.append(author)
			if user in authors:
				new_path.save()
				messages.success(request, 'New path created.')
			else:
				messages.error(request, 'You are not an author of this story. Path not created.')
		return redirect(reverse('author:storypage_update', kwargs={'storyslug':self.kwargs.get('storyslug'), 'storypageslug':self.kwargs.get('storypageslug')}))

class StoryPathDeleteView(StoryPathBase, View):
	def post(self, request, **kwargs):
		if request.method == 'POST':
			user = Profile.objects.get(user=self.request.user)
			story = Story.objects.get(slug=self.kwargs.get('storyslug'))
			storyowner_list = StoryOwner.objects.filter(story=story).values('user')
			authors = []
			for a in storyowner_list:
				author = Profile.objects.get(user=a['user'])
				authors.append(author)
		if user in authors:
			StoryPath.objects.get(pk=self.kwargs.get('pk')).delete()
			messages.success(request, 'Path removed.')
		else:
			messages.error(request, 'You are not an author of this story. Path not removed.')
		return redirect(reverse('author:storypage_update', kwargs={'storyslug':self.kwargs.get('storyslug'), 'storypageslug':self.kwargs.get('storypageslug')}))


# COMMENTS
class CommentCreate(LoginRequiredMixin, View):
	def post(self, request, **kwargs):
		if request.method == 'POST':
			form = CommentForm(request.POST)
			user = Profile.objects.get(user=self.request.user)
			story = Story.objects.get(slug=self.kwargs.get('storyslug'))
			storypage = StoryPage.objects.get(slug=self.kwargs.get('storypageslug'))
			storyowners = StoryOwner.objects.filter(story=story)
			authors = []
			for storyowner in storyowners:
				authors.append(storyowner.user.id)

		if form.is_valid():
			cd = form.cleaned_data
			new_comment = form.save(commit=False)
			new_comment.story = story
			new_comment.commenter = user
			new_comment.page = storypage
		
		if user.id in authors:
			new_comment.save()
			messages.success(request, 'New comment added to this page.')
		else:
			messages.error(request, 'You cannot comment on this story.')
		return redirect(reverse('author:storypage_update', kwargs={'storyslug':self.kwargs.get('storyslug'), 'storypageslug':self.kwargs.get('storypageslug')}))

class CommentUpdate(LoginRequiredMixin, FormView):

	# def get(self, request, **kwargs):
	# 	print('COMMENTUPDATE GET()')
	# 	context = self.get_context_data(**kwargs)
	# 	return self.render_to_response(context)

	# def get_context_data(self, request, **kwargs):
	# 	context['comment_data'] = Comment.objects.get(pk=self.kwargs.get('comment_pk'))
	# 	print('COMMENT: ',conext['comment_data'])
	# 	return context
	template_name = 'authoring/modals/add_comment.html'
	form_class = CommentForm

	def get_initial(self, request, **kwargs):
		initial = super().get_initial()
		initial['text']=Comment.objects.get(pk=self.kwargs.get('comment_pk')).values('text')
		print(initial)
		return initial

	def post(self, request, **kwargs):
		if request.method == 'POST':
			form = CommentForm(request.POST)
			user = Profile.objects.get(user=self.request.user)
			story = Story.objects.get(slug=self.kwargs.get('storyslug'))
			storypage = StoryPage.objects.get(slug=self.kwargs.get('storypageslug'))
			storyowners = StoryOwner.objects.filter(story=story)
			authors = []
			for storyowner in storyowners:
				authors.append(storyowner.user.id)

		if form.is_valid():
			cd = form.cleaned_data
			new_comment = form.save(commit=False)
			new_comment.story = story
			new_comment.commenter = user
			new_comment.page = storypage
		
		if user.id in authors:
			new_comment.save()
			messages.success(request, 'New comment added to this page.')
		else:
			messages.error(request, 'You cannot comment on this story.')
		return redirect(reverse('author:storypage_update', kwargs={'storyslug':self.kwargs.get('storyslug'), 'storypageslug':self.kwargs.get('storypageslug')}))

class CommentDelete(LoginRequiredMixin, View):
	def post(self, request, **kwargs):
		if request.method == 'POST':
			user = Profile.objects.get(user=self.request.user)
			story = Story.objects.get(slug=self.kwargs.get('storyslug'))
			storypage = StoryPage.objects.get(slug=self.kwargs.get('storypageslug'))
			storyowners = StoryOwner.objects.filter(story=story)
			authors = []
			for storyowner in storyowners:
				authors.append(storyowner.user.id)
		if user.id in authors:
			Comment.objects.get(pk=self.kwargs.get('comment_pk')).delete()
			messages.info(request, 'Comment deleted.')
		else:
			messages.error(request, 'You cannot delete a comment.')
		return redirect(reverse('author:storypage_update', kwargs={'storyslug':self.kwargs.get('storyslug'), 'storypageslug':self.kwargs.get('storypageslug')}))