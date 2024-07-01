from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from smart_media.admin import SmartAdminMixin

from ..admin.album import AlbumItemAdmin
from ..choices_helpers import (
    get_album_feature_choices,
    get_album_template_default,
)
from ..forms.album import AlbumForm
from ..models.album import Album


class AlbumPlugin(SmartAdminMixin, CMSPluginBase):
    """
    Album interface is able to add/edit/remove items within inline forms.

    Also used template is dynamically retrieved from "template" value.
    """
    module = _("Blocks")
    name = _("Album")
    model = Album
    form = AlbumForm
    inlines = (AlbumItemAdmin,)
    render_template = get_album_template_default()
    cache = True

    def get_fieldsets(self, request, obj=None):
        """
        Define plugin form fieldsets depending features are enabled or not (when there
        is no defined feature choices).
        """
        fieldsets = [
            (None, {
                "fields": (
                    "template",
                ),
            }),
            (_("Content"), {
                "fields": (
                    "title",
                ),
            }),
            (_("Options"), {
                "fields": (
                    "mass_upload",
                ),
            }),
        ]

        if len(get_album_feature_choices()) > 0:
            fieldsets.append((_("Features"), {
                "fields": (
                    "features",
                ),
            }))

        return tuple(fieldsets)

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template
        ressources = instance.album_item.all().order_by("order")
        context.update({
            "instance": instance,
            "ressources": ressources,
        })
        return context

    def save_model(self, request, obj, form, change):
        result = super().save_model(request, obj, form, change)

        # Save awaiting item in memory
        for item in getattr(obj, "_awaiting_items", []):
            item.album = obj
            item.save()

        return result
