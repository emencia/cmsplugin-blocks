# -*- coding: utf-8 -*-
"""
====
Hero
====

A hero component with an image (commonly for background) and a content.

"""
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.encoding import force_text
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from cmsplugin_blocks.choices_helpers import (get_hero_default_template,
                                              get_hero_template_choices)
from cmsplugin_blocks.utils import SmartFormatMixin


class Hero(SmartFormatMixin, CMSPlugin):
    """
    Hero component.
    """
    template = models.CharField(
        _("Template"),
        blank=False,
        max_length=150,
        choices=get_hero_template_choices(),
        default=get_hero_default_template(),
        help_text=_("Used template for content look."),
    )
    """
    Template choice from available plugin templates in setting
    ``BLOCKS_HERO_TEMPLATES``. Default to the first choice item.
    """

    image = models.FileField(
        _("Image"),
        upload_to="blocks/hero/%y/%m",
        max_length=255,
        blank=True,
        null=True,
        default=None,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.BLOCKS_ALLOWED_IMAGE_EXTENSIONS
            ),
        ]
    )
    """
    Optional image file, limited to enabled image formats from settings
    ``BLOCKS_ALLOWED_IMAGE_EXTENSIONS``.
    """

    content = models.TextField(
        _(u"Content"),
        blank=False,
        default="",
    )
    """
    Required long text, it will be editable through CKeditor on plugin form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = force_text(self.content)

    def __str__(self):
        return Truncator(strip_tags(self.content)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = _("Hero")
        verbose_name_plural = _("Heros")
