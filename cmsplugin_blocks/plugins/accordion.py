from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from smart_media.admin import SmartAdminMixin

from ..admin.accordion import AccordionItemAdmin
from ..choices_helpers import get_accordion_template_default
from ..forms.accordion import AccordionForm
from ..models.accordion import Accordion


class AccordionPlugin(SmartAdminMixin, CMSPluginBase):
    """
    Accordion interface is able to add/edit/remove accordion items as inline forms.
    """
    module = _("Blocks")
    name = _("Accordion")
    model = Accordion
    form = AccordionForm
    inlines = (AccordionItemAdmin,)
    render_template = get_accordion_template_default()
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
                    "keep_open",
                ),
            }),
            (_("Content"), {
                "fields": (
                    "title",
                ),
            }),
        ]

        display_features = True
        if display_features:
            fieldsets.append((_("Features"), {
                "fields": (
                    "size_features",
                    "color_features",
                    "extra_features",
                ),
            }))

        return tuple(fieldsets)

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template
        slides = instance.accordion_item.all().order_by("order")
        context.update({
            "instance": instance,
            "slides": slides,
        })
        return context
