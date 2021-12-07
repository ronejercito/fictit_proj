from django.urls import path, re_path, include
from .views import StoryIndexView, StoryCreateView, StoryDetailView

app_name='author'

urlpatterns = [
	re_path('', StoryIndexView.as_view(), name='story_index'),
	re_path('create/', StoryCreateView.as_view(), name='story_create'),
	# re_path('story/', include([
	# 	re_path('create/', StoryCreateView.as_view(), name='story_create'),
	# 	re_path('<slug:storyslug>/', include([
	# 		re_path('detail/', StoryDetailView.as_view(), name='story_detail'),
	# 		# re_path('update/', StoryUpdateView.as_view(), name='story_update'),
	# 		# re_path('delete/', StoryDeleteView.as_view(), name='story_delete'),
	# 	])),
	# ])),
]