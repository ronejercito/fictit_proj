from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext as _

from integrations.models import StoryPluginModel


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
	render_template = 'authoring/authoring_plugin.html'

	def render(self, context, instance, placeholder):
		context.update({'instance':instance})
		return context