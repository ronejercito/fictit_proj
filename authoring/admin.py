from django.contrib import admin
from cms.extensions import PageExtensionAdmin

# Register your models here.
from .models import Story, StoryPage, StoryOwner, StoryPath, Comment, Response

# class StoryExtensionAdmin(PageExtensionAdmin):
# 	pass

# class StoryPageExtensionAdmin(PageExtensionAdmin):
# 	pass

admin.site.register(Story)
admin.site.register(StoryPage)
admin.site.register(StoryOwner)
admin.site.register(StoryPath)

admin.site.register(Comment)
admin.site.register(Response)