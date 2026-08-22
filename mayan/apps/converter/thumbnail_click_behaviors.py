from django.utils.translation import gettext_lazy as _

from .classes import ThumbnailClickBehaviorBackend


class ThumbnailClickBehaviorBackendImagePreview(ThumbnailClickBehaviorBackend):
    label = _(message='Image preview')
    name = 'image_preview'
    template_name = 'converter/thumbnail_click_behaviors/image_preview.html'

    def get_anchor_context(self):
        return {'gallery_name': self.gallery_name}
