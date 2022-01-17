from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext as _

from integrations.models import StoryPluginModel, StoryOwnerPluginModel, StoryPagePluginModel


@plugin_pool.register_plugin
class HelloPlugin(CMSPluginBase):
	model = CMSPlugin
	render_template = "hello_plugin.html"
	cache = False

@plugin_pool.register_plugin
class AuthoringPlugin(CMSPluginBase):
	model = StoryPluginModel
	name = _('Story Plugin')
	module = _('Authoring')
	render_template = 'authoring/plugin/authoring_plugin.html'

	def render(self, context, instance, placeholder):
		context.update({'instance':instance})
		return context

@plugin_pool.register_plugin
class StoryOwnerPlugin(CMSPluginBase):
	model = StoryOwnerPluginModel
	name = _('Story Owner Plugin')
	module = _('Authoring')
	render_template = 'authoring/plugin/storyowner_plugin.html'

	def render(self, context, instance, placeholder):
		context.update({'instance':instance})
		return context

@plugin_pool.register_plugin
class StoryPagePlugin(CMSPluginBase):
	model = StoryPagePluginModel
	name = _('Story Page Plugin')
	module = _('Authoring')
	render_template = 'authoring/plugin/storypage_plugin.html'

	def render(self, context, instance, placeholder):
		context.update({'instance':instance})
		return context