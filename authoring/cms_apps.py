from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class AuthoringAppHook(CMSApp):
	app_name = 'authoring'
	name = 'Authoring App'

	def get_urls(self, page=None, language=None, **kwargs):
		return ['authoring.urls']