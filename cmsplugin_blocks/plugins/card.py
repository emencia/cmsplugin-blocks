# -*- coding: utf-8 -*-
"""
Card CMS Plugin interface definitions
"""
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from cmsplugin_blocks.choices_helpers import get_card_default_template

from cmsplugin_blocks.models.card import Card
from cmsplugin_blocks.forms.card import CardForm


class CardPlugin(CMSPluginBase):
    module = _('Blocks')
    name = _("Card")
    model = Card
    form = CardForm
    render_template = get_card_default_template()
    cache = True
    fieldsets = (
        (None, {
            'fields': (
                ('alignment', 'template'),
                'image',
                'content',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template

        context.update({
            'instance': instance,
        })

        return context
