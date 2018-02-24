# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from cmsplugin_blocks.choices_helpers import (get_card_default_template,
                                              get_card_template_choices)

@python_2_unicode_compatible
class Card(CMSPlugin):
    """
    A simple card object
    """
    ALIGNMENT_CHOICES = [
        ('left', _('Content to the left, image to the right')),
        ('right', _('Image to the left, content to the reft')),
    ]

    alignment = models.CharField(
        _('Alignment'),
        choices=ALIGNMENT_CHOICES,
        max_length=15,
        blank=False,
        default='left',
    )
    template = models.CharField(
        _('Template'),
        blank=False,
        max_length=150,
        choices=get_card_template_choices(),
        default=get_card_default_template(),
        help_text=_('Used template for content look.'),
    )
    image = models.ImageField(
        _('Image'),
        upload_to='blocks/card/%y/%m',
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )
    content = models.TextField(
        _(u"Content"),
        blank=False,
        default="",
    )

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)
        self.content = force_text(self.content)

    def __str__(self):
        return Truncator(strip_tags(self.content)).words(4, truncate="...")

    def save(self, *args, **kwargs):
        super(Card, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')
