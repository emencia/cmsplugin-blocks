# -*- coding: utf-8 -*-
"""
Hero CMS Plugin interface definitions
"""
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from cmsplugin_blocks.choices_helpers import get_hero_default_template

from cmsplugin_blocks.models.hero import Hero
from cmsplugin_blocks.forms.hero import HeroForm


class HeroPlugin(CMSPluginBase):
    module = _('Blocks')
    name = _("Hero")
    model = Hero
    form = HeroForm
    render_template = get_hero_default_template()
    cache = True
    fieldsets = (
        (None, {
            'fields': (
                'template',
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
