from django.urls import path, re_path, include
from .views import (
	StoryIndexView, StoryCreateView, StoryDetailView, StoryDeleteView,
	StoryOwnerCreator, StoryOwnerDeleteView,
	StoryPageCreateView, StoryPageDetailView, StoryPageUpdateView, StoryPageDeleteView,
	StoryPathCreateView, StoryPathDeleteView,
	CommentCreate, CommentUpdate, CommentDelete
)

app_name='author'

urlpatterns = [
	path('', StoryIndexView.as_view(), name='story_index'),
	path('create/', StoryCreateView.as_view(), name='story_create'),
	# path('test/', StoryPageCreateView.as_view(), name='storypage_create'),
	path('<slug:storyslug>/', include([
		path('detail/', StoryDetailView.as_view(), name='story_detail'),
		path('add_author/', StoryDetailView.as_view(template_name='authoring/modals/add_author.html'), name='story_detail_add_author'),
		# path('update/', StoryUpdateView.as_view(), name='story_update')
		path('delete/', StoryDeleteView.as_view(), name='story_delete'),

		path('<str:username>/', StoryOwnerCreator.as_view(), name='storyowner_create'),
		path('storyowners/<int:pk>/', StoryOwnerDeleteView.as_view(), name='storyowner_delete'),

		path('page/', include([
			path('new_page/', StoryPageCreateView.as_view(), name='storypage_create'),
			path('<slug:storypageslug>/', include([
				path('', StoryPageDetailView.as_view(), name='storypage_detail'),
				path('edit/', StoryPageUpdateView.as_view(), name='storypage_update'),
				path('delete/', StoryPageDeleteView.as_view(), name='storypage_delete'),

				path('path/', include([
					path('add_path/', StoryPageUpdateView.as_view(template_name='authoring/modals/add_path.html'), name='storypage_detail_add_path'),
					path('create/', StoryPathCreateView.as_view(), name='storypath_create'),
					path('delete_path/<int:pk>/', StoryPathDeleteView.as_view(), name='storypath_delete'),
				])),

				path('comment/', include([
					path('add_comment/', CommentCreate.as_view(), name='comment_create'),
					path('<int:comment_pk>/', include([
						path('update/', CommentUpdate.as_view(), name='comment_update'),
						path('delete/', CommentDelete.as_view(), name='comment_delete'),
					])),
				])),
			])), 
		])),
	])),
]