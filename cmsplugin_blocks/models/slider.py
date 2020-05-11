# -*- coding: utf-8 -*-
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
    Slide container
    """
    title = models.CharField(
        _('Title'),
        blank=False,
        max_length=150,
        default="",
    )
    template = models.CharField(
        _('Template'),
        blank=False,
        max_length=150,
        choices=get_slider_template_choices(),
        default=get_slider_default_template(),
        help_text=_('Used template for content look.'),
    )

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
        """
        self.slide_item.all().delete()

        for slide_item in oldinstance.slide_item.all():
            slide_item.pk = None
            slide_item.slider = self
            slide_item.save()

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')


class SlideItem(SmartFormatMixin, models.Model):
    """
    Slide item
    """
    slider = models.ForeignKey(
        Slider,
        related_name="slide_item",
        on_delete=models.CASCADE
    )
    title = models.CharField(
        _('Title'),
        blank=False,
        max_length=150,
        default="",
    )
    image = models.FileField(
        _('Image'),
        upload_to='blocks/slider/%y/%m',
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
    content = models.TextField(
        _(u"Content"),
        blank=True,
        default="",
    )
    order = models.IntegerField(
        _('Order'),
        blank=False,
        default=0
    )
    link_name = models.CharField(
        _('link name'),
        blank=True,
        max_length=45,
    )
    link_url = models.CharField(
        _('link url'),
        blank=True,
        max_length=255,
    )
    link_open_blank = models.BooleanField(
        _('open new window'),
        default=False,
        help_text=_('If checked the link will be open in a new window'),
    )

    def __str__(self):
        return Truncator(strip_tags(self.title)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = _('Slide item')
        verbose_name_plural = _('Slide items')
