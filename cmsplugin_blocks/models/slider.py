# -*- coding: utf-8 -*-
"""
======
Slider
======

A slideshow component which may be similar to Album but with difference that
a slide item can have HTML content.

Slide items are ordered from their ``order`` field value. Items with a zero
value for their order will be ordered in an almost arbitrary order (mostly
depending from item object id).

"""
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from cmsplugin_blocks.choices_helpers import (get_slider_default_template,
                                              get_slider_template_choices)
from cmsplugin_blocks.utils import SmartFormatMixin


class Slider(CMSPlugin):
    """
    Slide container for items.
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
        choices=get_slider_template_choices(),
        default=get_slider_default_template(),
        help_text=_("Used template for content look."),
    )
    """
    Template choice from available plugin templates in setting
    ``BLOCKS_SLIDER_TEMPLATES``. Default to the first choice item.
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
        self.slide_item.all().delete()

        for slide_item in oldinstance.slide_item.all():
            slide_item.pk = None
            slide_item.slider = self
            slide_item.save()

    class Meta:
        verbose_name = _("Slider")
        verbose_name_plural = _("Sliders")


class SlideItem(SmartFormatMixin, models.Model):
    """
    Slide item to include in container.
    """
    slider = models.ForeignKey(
        Slider,
        related_name="slide_item",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        _("Title"),
        blank=False,
        max_length=150,
        default="",
    )
    """
    Required title string.
    """

    image = models.FileField(
        _("Image"),
        upload_to="blocks/slider/%y/%m",
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

    content = models.TextField(
        _(u"Content"),
        blank=True,
        default="",
    )
    """
    Optional long text, it will be editable through CKeditor on plugin form.
    """

    order = models.IntegerField(
        _("Order"),
        blank=False,
        default=0
    )
    """
    Number for order position in item list.
    """

    link_name = models.CharField(
        _("link name"),
        blank=True,
        max_length=45,
    )
    """
    Optional string for link name.
    """

    link_url = models.CharField(
        _("link url"),
        blank=True,
        max_length=255,
    )
    """
    Optional string for link URL.
    """

    link_open_blank = models.BooleanField(
        _("open new window"),
        default=False,
        help_text=_("If checked the link will be open in a new window"),
    )
    """
    Checkbox to enable opening link URL in a new window/tab.
    """

    def __str__(self):
        return Truncator(strip_tags(self.title)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = _("Slide item")
        verbose_name_plural = _("Slide items")
