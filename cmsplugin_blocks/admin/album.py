from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from smart_media.admin import SmartModelAdmin

from ..choices_helpers import get_albumitem_feature_choices
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
        if len(get_albumitem_feature_choices()) > 0:
            fieldsets = (
                (None, {
                    "fields": (
                        "album",
                        "title",
                        "order",
                        "features",
                        "image",
                    ),
                }),
            )
        else:
            fieldsets = (
                (None, {
                    "fields": (
                        "album",
                        "title",
                        "order",
                        "image",
                    ),
                }),
            )

        return fieldsets
