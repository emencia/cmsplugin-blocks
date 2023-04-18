from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from ..choices_helpers import (
    get_hero_feature_choices,
    get_hero_template_default,
)
from ..forms.hero import HeroForm
from ..models.hero import Hero


class HeroPlugin(CMSPluginBase):
    module = _("Blocks")
    name = _("Hero")
    model = Hero
    form = HeroForm
    render_template = get_hero_template_default()
    cache = True

    def get_fieldsets(self, request, obj=None):
        if len(get_hero_feature_choices()) > 0:
            fieldsets = (
                (None, {
                    "fields": (
                        "template",
                        "features",
                        "image",
                        "content",
                    ),
                }),
            )
        else:
            fieldsets = (
                (None, {
                    "fields": (
                        "template",
                        "image",
                        "content",
                    ),
                }),
            )

        return fieldsets

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template

        context.update({
            "instance": instance,
        })

        return context
