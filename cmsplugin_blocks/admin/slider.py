# -*- coding: utf-8 -*-
"""
Slider admin interface
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from cmsplugin_blocks.models.slider import SlideItem
from cmsplugin_blocks.forms.slider import SlideItemForm


class SlideItemAdmin(admin.StackedInline):
    """
    Plugin admin form to enable inline mode inside SliderPlugin
    """
    model = SlideItem
    form = SlideItemForm
    extra = 0
    verbose_name = _("Slide")
    ordering = ["order"]
    fieldsets = (
        (None, {
            "fields": (
                "slider",
                "title",
                (
                    "image",
                    "order",
                ),
                "content",
                (
                    "link_name",
                    "link_url",
                ),
                "link_open_blank",
            ),
        }),
    )
