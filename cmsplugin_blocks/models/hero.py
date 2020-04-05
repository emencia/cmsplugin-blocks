# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.encoding import force_text
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from cmsplugin_blocks.choices_helpers import (get_hero_default_template,
                                              get_hero_template_choices)
from cmsplugin_blocks.utils import SmartFormatMixin


class Hero(SmartFormatMixin, CMSPlugin):
    """
    A simple hero content with image and HTML content
    """
    template = models.CharField(
        _('Template'),
        blank=False,
        max_length=150,
        choices=get_hero_template_choices(),
        default=get_hero_default_template(),
        help_text=_('Used template for content look.'),
    )
    image = models.FileField(
        _('Image'),
        upload_to='blocks/hero/%y/%m',
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
    content = models.TextField(
        _(u"Content"),
        blank=False,
        default="",
    )

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
        verbose_name = _('Hero')
        verbose_name_plural = _('Heros')
