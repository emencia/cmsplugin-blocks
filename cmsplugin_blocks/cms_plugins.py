# -*- coding: utf-8 -*-
"""
CMS Plugin interface definitions
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_blocks.models.banner import Banner
from cmsplugin_blocks.forms.banner import BannerForm

from cmsplugin_blocks.models.diptych import Diptych
from cmsplugin_blocks.forms.diptych import DiptychForm

from cmsplugin_blocks.models.slider import Slider, SlideItem
from cmsplugin_blocks.models.slider import get_template_default
from cmsplugin_blocks.forms.slider import SliderForm, SlideItemForm

from cmsplugin_blocks.models.establishment_opening import (
    EstablishmentOpening, DayItem
)
from cmsplugin_blocks.forms.establishment_opening import (
    EstablishmentOpeningForm, DayItemForm
)


class BannerPlugin(CMSPluginBase):
    module = _('Blocks')
    name = _("Banner")
    model = Banner
    form = BannerForm
    render_template = 'cmsplugin_blocks/banner.html'
    cache = True
    fieldsets = (
        (None, {
            'fields': (
                'background',
                'content',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
        })
        return context


class DiptychPlugin(CMSPluginBase):
    module = _('Blocks')
    name = _("Diptych")
    model = Diptych
    form = DiptychForm
    render_template = 'cmsplugin_blocks/diptych.html'
    cache = True
    fieldsets = (
        (None, {
            'fields': (
                'alignment',
                'image',
                'content',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
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
    render_template = get_template_default()
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


class DayItemAdmin(admin.StackedInline):
    """
    Admin interface to enable inline mode for items inside OpeningHours plugin
    """
    model = DayItem
    form = DayItemForm
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'opening',
                'name',
                'hours',
            ),
        }),
    )


class EstablishmentOpeningPlugin(CMSPluginBase):
    """
    EstablishmentOpeningForm interface is able to add/edit/remove day items
    as inline forms.
    """
    module = _('Blocks')
    name = _("Establishment opening")
    model = EstablishmentOpening
    form = EstablishmentOpeningForm
    inlines = (DayItemAdmin,)
    render_template = 'cmsplugin_blocks/establishment_opening.html'
    cache = True
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'comment',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(EstablishmentOpeningPlugin, self).render(context, instance, placeholder)
        days = instance.day_item.all()
        context.update({
            'instance': instance,
            'days': days,
        })
        return context


plugin_pool.register_plugin(BannerPlugin)
plugin_pool.register_plugin(DiptychPlugin)
plugin_pool.register_plugin(SliderPlugin)
plugin_pool.register_plugin(EstablishmentOpeningPlugin)
