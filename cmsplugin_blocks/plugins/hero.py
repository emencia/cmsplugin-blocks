from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from smart_media.admin import SmartAdminMixin

from ..choices_helpers import get_hero_template_default
from ..forms.hero import HeroForm
from ..models.hero import Hero


class HeroPlugin(SmartAdminMixin, CMSPluginBase):
    module = _("Blocks")
    name = _("Hero")
    model = Hero
    form = HeroForm
    render_template = get_hero_template_default()
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
                    "image",
                    "content",
                ),
            }),
            (_("Options"), {
                "fields": (
                    "image_alt",
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

        context.update({
            "instance": instance,
        })

        return context
