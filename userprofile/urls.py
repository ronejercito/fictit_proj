from django.urls import path, re_path, include
from .views import ProfileDetailView, ProfileCreateView, ProfileUpdateView

app_name='profile'

urlpatterns = [
	path('<str:username>/', include([
		path('', ProfileDetailView.as_view(), name='profile_detail'),
		path('create/', ProfileCreateView.as_view(), name='profile_create'),
		path('update/', ProfileUpdateView.as_view(), name='profile_update'),
	])),
]