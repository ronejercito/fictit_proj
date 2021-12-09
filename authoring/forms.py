from django import forms

from .models import Story, StoryOwner

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story
		fields = ['title']

		# def save(self, commit=True):
		# 	print('SAVING FORM')
		# 	story = super(StoryForm, self).save(commit=False)
		# 	story.started_by = self.user
		# 	print(story.started_by)
		# 	if commit:
		# 		story.save()
		# 	return story