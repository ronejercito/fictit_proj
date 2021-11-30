from django.contrib import admin
from cms.extensions import PageExtensionAdmin

# Register your models here.
from .models import Story, StoryPage

class StoryExtensionAdmin(PageExtensionAdmin):
	pass

class StoryPageExtensionAdmin(PageExtensionAdmin):
	pass

admin.site.register(Story, StoryExtensionAdmin)
admin.site.register(StoryPage, StoryPageExtensionAdmin)