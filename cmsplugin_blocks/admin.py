# -*- coding: utf-8 -*-
"""
Admin interface definitions
"""
import logging

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail import get_thumbnail

from cmsplugin_blocks.models.album import AlbumItem
from cmsplugin_blocks.forms.album import AlbumItemForm

from cmsplugin_blocks.models.slider import SlideItem
from cmsplugin_blocks.forms.slider import SlideItemForm


class AlbumItemAdmin(admin.TabularInline):
    """
    Plugin admin form to enable inline mode inside AlbumPlugin
    """
    model = AlbumItem
    form = AlbumItemForm
    extra = 0
    verbose_name = _("Image")
    ordering = ['order']
    template = "cmsplugin_blocks/admin/albumitem_edit_tabular.html"
    fieldsets = (
        (None, {
            'fields': (
                'admin_thumbnail',
                'album',
                'title',
                'order',
                'image',
            ),
        }),
    )
    readonly_fields = ('admin_thumbnail',)

    def admin_thumbnail(self, obj):
        tag = (
            """<a href="{source}" target="blank">"""
            """<img src="{thumb}" alt="">"""
            """</a>"""
        )
        try:
            return tag.format(
                source=obj.image.url,
                thumb=get_thumbnail(obj.image, '80x80', crop='center').url
            )
        except IOError:
            logger = logging.getLogger("cmsplugin_blocks.admin.albumitem")
            logger.exception('IOError for image {}'.format(obj.image))
            return 'IOError'
        except ThumbnailError as ex:
            return "ThumbnailError, {}".format(ex.message)

    admin_thumbnail.short_description = 'Current'
    admin_thumbnail.allow_tags = True


class SlideItemAdmin(admin.StackedInline):
    """
    Plugin admin form to enable inline mode inside SliderPlugin
    """
    model = SlideItem
    form = SlideItemForm
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'slider',
                'image',
                'content',
                (
                    'order',
                    'link_name',
                    'link_url',
                    'link_open_blank',
                ),
            ),
        }),
    )
