# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from cmsplugin_blocks.choices_helpers import (get_hero_default_template,
                                              get_hero_template_choices)

@python_2_unicode_compatible
class Hero(CMSPlugin):
    """
    A very simple banner with background image and HTML content
    """
    template = models.CharField(
        _('Template'),
        blank=True,
        max_length=100,
        choices=get_hero_template_choices(),
        default=get_hero_default_template(),
        help_text=_('Used template for content look.'),
    )
    background = models.ImageField(
        _('Background image'),
        upload_to='blocks/hero/%y/%m',
        max_length=255,
        null=True,
        default=None,
    )
    content = models.TextField(
        _(u"Content"),
        default="",
    )

    def __init__(self, *args, **kwargs):
        super(Hero, self).__init__(*args, **kwargs)
        self.content = force_text(self.content)

    def __str__(self):
        return Truncator(strip_tags(self.content)).words(4, truncate="...")

    def save(self, *args, **kwargs):
        super(Hero, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Hero')
        verbose_name_plural = _('Heros')
