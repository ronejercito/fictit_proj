from django import forms

from .models import Story, StoryOwner, StoryPage, StoryPath, Comment

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story
		fields = ['title']

class StoryPageForm(forms.ModelForm):
	fieldsets = [
		(None, {'fields':['challenge', 'start', 'end', 'publish']})
	]

	class Meta:
		model = StoryPage
		fields = ['title', 'text', 'challenge', 'start', 'end', 'publish']

class StoryPathForm(forms.ModelForm):
	class Meta:
		model = StoryPath
		fields = ['storypath', 'correct']

	def __init__(self, storyslug, storypageslug, *args, **kwargs):
		# FILTER SELECTION TO PAGES IN THIS STORY EXCLUDING CURRENT PAGE
		super(StoryPathForm, self).__init__(*args, **kwargs)
		story = Story.objects.get(slug=storyslug)
		self.fields['storypath'].queryset = StoryPage.objects.filter(story=story).exclude(slug=storypageslug)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
	class Meta: 
		model = Comment
		fields = ['text', 'quote', 'resolved', ]