# -*- coding: utf-8 -*-
"""
Slider CMS Plugin interface definitions
"""
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from cmsplugin_blocks.admin import SlideItemAdmin

from cmsplugin_blocks.choices_helpers import get_slider_default_template

from cmsplugin_blocks.models.slider import Slider
from cmsplugin_blocks.forms.slider import SliderForm


class SliderPlugin(CMSPluginBase):
    """
    Slider interface is able to add/edit/remove slide items as inline forms.

    Also used template is dynamically retrieved from 'template' value.
    """
    module = _('Blocks')
    name = _("Slider")
    model = Slider
    form = SliderForm
    inlines = (SlideItemAdmin,)
    render_template = get_slider_default_template()
    cache = True
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'template',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template
        slides = instance.slide_item.all().order_by('order')
        context.update({
            'instance': instance,
            'slides': slides,
        })
        return context
