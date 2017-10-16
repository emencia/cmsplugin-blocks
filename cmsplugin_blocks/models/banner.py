# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class Banner(CMSPlugin):
    """
    A very simple banner with background image and HTML content
    """
    background = models.ImageField(
        _('Background image'),
        upload_to='blocks/banner/%y/%m',
        max_length=255,
        null=True,
        default=None,
    )
    content = models.TextField(
        _(u"Content"),
        default="",
    )

    def __init__(self, *args, **kwargs):
        super(Banner, self).__init__(*args, **kwargs)
        self.content = force_text(self.content)

    def __str__(self):
        return Truncator(strip_tags(self.content)).words(4, truncate="...")

    def save(self, *args, **kwargs):
        super(Banner, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
