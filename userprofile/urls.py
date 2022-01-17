from django.urls import path, re_path, include
from .views import (
	ProfileDetailView, ProfileUpdateView, MyGroupListView, SearchUserView,
	ProfileConnectionListView, ProfileConnectionCreateView, ProfileConnectionDeleteView,
)

app_name='profile'

urlpatterns = [
	path('search/', include([
		path('', SearchUserView.as_view(), name='search'),
		path('<slug:storyslug>/', SearchUserView.as_view(), name='search_story'),
		])),
	path('<slug:storyslug>/', MyGroupListView.as_view(), name='groups_story'),
	path('<str:username>/', include([
		path('', ProfileDetailView.as_view(), name='profile_detail'),
		# path('create/', ProfileCreateView.as_view(), name='profile_create'),
		path('update/', ProfileUpdateView.as_view(), name='profile_update'),
		path('mygroups/', include([
			path('', MyGroupListView.as_view(), name='groups'),
		# 	path('<slug:storyslug>/', MyGroupListView.as_view(), name='groups_story'),
			])),

		path('connections/', include([
			path('', ProfileConnectionListView.as_view(), name='profileconnection_list'),
			path('create/', ProfileConnectionCreateView.as_view(), name='profileconnection_create'),
			path('delete/', ProfileConnectionDeleteView.as_view(), name='profileconnection_delete'),
		])),
	])),
]