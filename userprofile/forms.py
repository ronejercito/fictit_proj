from django import forms

from .models import Profile, ProfileConnection

# class ProfileForm(forms.ModelForm):
# 	class Meta:
# 		model = Profile
# 		fields = ['user']

class ProfileConnectionForm(forms.ModelForm):
	class Meta:
		template_name = 'userprofile/profileconnection_form.html'
		model = ProfileConnection
		fields = ['profile', 'contact']

class SearchUserForm(forms.Form):
	query = forms.CharField()