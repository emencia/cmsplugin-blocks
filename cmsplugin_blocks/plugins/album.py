# -*- coding: utf-8 -*-
"""
CMS Plugin interface definitions
"""
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from cmsplugin_blocks.admin import AlbumItemAdmin

from cmsplugin_blocks.choices_helpers import get_album_default_template

from cmsplugin_blocks.models.album import Album
from cmsplugin_blocks.forms.album import AlbumForm


class AlbumPlugin(CMSPluginBase):
    """
    Album interface is able to add/edit/remove items within inline forms.

    Also used template is dynamically retrieved from 'template' value.
    """
    module = _('Blocks')
    name = _("Album")
    model = Album
    form = AlbumForm
    inlines = (AlbumItemAdmin,)
    render_template = get_album_default_template()
    cache = True
    fieldsets = (
        (None, {
            'fields': (
                'title',
                ('template', 'mass_upload'),
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template
        ressources = instance.album_item.all().order_by('order')
        context.update({
            'instance': instance,
            'ressources': ressources,
        })
        return context

    def save_model(self, request, obj, form, change):
        result = super().save_model(request, obj, form, change)

        # Save awaiting item in memory
        for item in getattr(obj, '_awaiting_items', []):
            item.album = obj
            item.save()

        return result
