from cms.toolbar_pool import toolbar_pool
from cms.extensions.toolbar import ExtensionToolbar
from django.utils.translation import gettext_lazy as _
from .models import Story

# @toolbar_pool.register
# class StoryExtensionToolbar(ExtensionToolbar):
# 	model = Story

# 	def populate(self):
# 		current_page_menu = self._setup_extension_toolbar()
# 		if current_page_menu:
# 			page_extension, url = self.get_page_extension_admin()
# 			if url:
# 				current_page_menu.add_modal_item(_('Story'), url=url, disabled=not self.toolbar.edit_mode_active, position=0)