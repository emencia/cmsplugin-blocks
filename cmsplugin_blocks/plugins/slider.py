from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from smart_media.admin import SmartAdminMixin

from ..admin.slider import SlideItemAdmin
from ..choices_helpers import (
    get_slider_feature_choices,
    get_slider_template_default,
)
from ..forms.slider import SliderForm
from ..models.slider import Slider


class SliderPlugin(SmartAdminMixin, CMSPluginBase):
    """
    Slider interface is able to add/edit/remove slide items as inline forms.
    """
    module = _("Blocks")
    name = _("Slider")
    model = Slider
    form = SliderForm
    inlines = (SlideItemAdmin,)
    render_template = get_slider_template_default()
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
        ]

        if len(get_slider_feature_choices()) > 0:
            fieldsets.append((_("Features"), {
                "fields": (
                    "features",
                ),
            }))

        return tuple(fieldsets)

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template
        slides = instance.slide_item.all().order_by("order")
        context.update({
            "instance": instance,
            "slides": slides,
        })
        return context
