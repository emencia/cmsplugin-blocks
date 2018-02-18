# -*- coding: utf-8 -*-
"""
CMS Plugin interface definitions
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_blocks.choices_helpers import (get_card_default_template,
                                              get_hero_default_template,
                                              get_slider_default_template)

from cmsplugin_blocks.models.card import Card
from cmsplugin_blocks.forms.card import CardForm

from cmsplugin_blocks.models.hero import Hero
from cmsplugin_blocks.forms.hero import HeroForm

from cmsplugin_blocks.models.slider import Slider, SlideItem
from cmsplugin_blocks.forms.slider import SliderForm, SlideItemForm


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
                'alignment',
                'template',
                'image',
                'content',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(CardPlugin, self).render(context, instance,
                                                 placeholder)
        self.render_template = instance.template

        context.update({
            'instance': instance,
        })

        return context


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
                'background',
                'content',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(HeroPlugin, self).render(context, instance,
                                                 placeholder)
        self.render_template = instance.template

        context.update({
            'instance': instance,
        })

        return context


class SlideItemAdmin(admin.StackedInline):
    """
    Admin interface to enable inline mode for items inside Slider plugin
    """
    model = SlideItem
    form = SlideItemForm
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'slider',
                'background',
                'content',
                (
                    'link_name',
                    'link_url',
                    'link_open_blank',
                ),
            ),
        }),
    )


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
        context = super(SliderPlugin, self).render(context, instance,
                                                   placeholder)
        self.render_template = instance.template
        slides = instance.slide_item.all()
        context.update({
            'instance': instance,
            'slides': slides,
        })
        return context


plugin_pool.register_plugin(HeroPlugin)
plugin_pool.register_plugin(CardPlugin)
plugin_pool.register_plugin(SliderPlugin)
