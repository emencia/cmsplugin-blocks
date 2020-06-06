# -*- coding: utf-8 -*-
"""
=====
Album
=====

An album component you may use in a gallery.

Album items are ordered from their ``order`` field value. Items with a zero
value for their order will be ordered in an almost arbitrary order (mostly
depending from item object id).

Album form have a special field ``mass_upload``, it expects a valid ZIP archive
file to create items. Archive file is limited to the value from setting
``BLOCKS_MASSUPLOAD_FILESIZE_LIMIT``.

The archive file may contains one or many image files with enabled format from
setting ``BLOCKS_ALLOWED_IMAGE_EXTENSIONS``. Each image will create a new Album
item where the name will be filled with the full relative image file path. Images
in archive can be structured in multiple subdirectory. Created Album item from
an archive don't have any order.

"""
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from cmsplugin_blocks.choices_helpers import (get_album_default_template,
                                              get_album_template_choices)
from cmsplugin_blocks.utils import SmartFormatMixin


class Album(CMSPlugin):
    """
    Album container for items.
    """
    title = models.CharField(
        _("Title"),
        blank=False,
        max_length=150,
        default="",
    )
    """
    A required title string.
    """

    template = models.CharField(
        _("Template"),
        blank=False,
        max_length=150,
        choices=get_album_template_choices(),
        default=get_album_default_template(),
        help_text=_("Used template for content formatting."),
    )
    """
    Template choice from available plugin templates in setting
    ``BLOCKS_ALBUM_TEMPLATES``. Default to the first choice item.
    """

    def __str__(self):
        return Truncator(strip_tags(self.title)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def copy_relations(self, oldinstance):
        """
        Copy FK relations when plugin object is copied as another object

        See:

        http://docs.django-cms.org/en/latest/how_to/custom_plugins.html#for-foreign-key-relations-from-other-objects

        :meta private:
        """
        self.album_item.all().delete()

        for album_item in oldinstance.album_item.all():
            album_item.pk = None
            album_item.album = self
            album_item.save()

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")


class AlbumItem(SmartFormatMixin, models.Model):
    """
    Album item to include in container.
    """
    album = models.ForeignKey(
        Album,
        related_name="album_item",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        _("Title"),
        blank=True,
        max_length=150,
        default="",
    )
    """
    Optional title string.
    """

    order = models.IntegerField(
        _("Order"),
        blank=False,
        default=0
    )
    """
    Number for order position in item list.
    """

    image = models.FileField(
        _("Image"),
        upload_to="blocks/album/%y/%m",
        max_length=255,
        null=True,
        blank=False,
        default=None,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.BLOCKS_ALLOWED_IMAGE_EXTENSIONS
            ),
        ]
    )
    """
    Required image file, limited to enabled image formats from settings
    ``BLOCKS_ALLOWED_IMAGE_EXTENSIONS``.
    """

    def __str__(self):
        return Truncator(strip_tags(self.title)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = _("Album item")
        verbose_name_plural = _("Album items")
