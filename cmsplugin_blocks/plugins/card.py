from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from ..choices_helpers import (
    get_card_feature_choices,
    get_card_template_default,
)
from ..forms.card import CardForm
from ..models.card import Card


class CardPlugin(CMSPluginBase):
    module = _("Blocks")
    name = _("Card")
    model = Card
    form = CardForm
    render_template = get_card_template_default()
    cache = True

    def get_fieldsets(self, request, obj=None):
        if len(get_card_feature_choices()) > 0:
            fieldsets = (
                (None, {
                    "fields": (
                        "title",
                        "template",
                        (
                            "features",
                            "image",
                        ),
                        (
                            "link_url",
                            "link_open_blank",
                        ),
                        "content",
                    ),
                }),
            )
        else:
            fieldsets = (
                (None, {
                    "fields": (
                        "title",
                        "template",
                        "image",
                        (
                            "link_url",
                            "link_open_blank",
                        ),
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
