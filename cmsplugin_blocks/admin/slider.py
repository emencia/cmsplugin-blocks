from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from smart_media.admin import SmartModelAdmin

from ..models.slider import SlideItem
from ..forms.slider import SlideItemForm


class SlideItemAdmin(admin.StackedInline):
    """
    Plugin admin form to enable inline mode inside SliderPlugin
    """
    model = SlideItem
    form = SlideItemForm
    extra = 0
    verbose_name = _("Slide")
    ordering = ["order"]
    formfield_overrides = SmartModelAdmin.formfield_overrides

    def get_fieldsets(self, request, obj=None):
        """
        Define plugin form fieldsets depending features are enabled or not (when there
        is no defined feature choices).
        """
        fieldsets = [
            (None, {
                "fields": (
                    "slider",
                ),
            }),
            (_("Content"), {
                "fields": (
                    "title",
                    "image",
                    (
                        "link_name",
                        "link_url",
                    ),
                    "content",
                ),
            }),
            (_("Options"), {
                "fields": (
                    "order",
                    "image_alt",
                    "link_open_blank",
                ),
            }),
        ]

        return tuple(fieldsets)
