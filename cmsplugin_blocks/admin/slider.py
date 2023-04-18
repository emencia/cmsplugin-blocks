from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from smart_media.admin import SmartModelAdmin

from ..choices_helpers import get_slideritem_feature_choices
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
        if len(get_slideritem_feature_choices()) > 0:
            fieldsets = (
                (None, {
                    "fields": (
                        "slider",
                        "title",
                        (
                            "image",
                            "order",
                            "features",
                        ),
                        "content",
                        (
                            "link_name",
                            "link_url",
                        ),
                        "link_open_blank",
                    ),
                }),
            )
        else:
            fieldsets = (
                (None, {
                    "fields": (
                        "slider",
                        "title",
                        (
                            "image",
                            "order",
                        ),
                        "content",
                        (
                            "link_name",
                            "link_url",
                        ),
                        "link_open_blank",
                    ),
                }),
            )

        return fieldsets
