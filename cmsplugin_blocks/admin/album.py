from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from smart_media.admin import SmartModelAdmin

from ..models.album import AlbumItem
from ..forms.album import AlbumItemForm


class AlbumItemAdmin(admin.TabularInline):
    """
    Plugin admin form to enable inline mode inside AlbumPlugin
    """
    model = AlbumItem
    form = AlbumItemForm
    extra = 0
    verbose_name = _("Image")
    ordering = ["order"]
    template = "cmsplugin_blocks/admin/albumitem_edit_tabular.html"
    formfield_overrides = SmartModelAdmin.formfield_overrides

    def get_fieldsets(self, request, obj=None):
        fields = [
            "album",
            "title",
            "order",
            "image",
            "image_alt",
        ]

        return (
            (None, {
                "fields": tuple(fields),
            }),
        )
