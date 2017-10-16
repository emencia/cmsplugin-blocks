# -*- coding: utf-8 -*-
"""
WARNING: Every created new migration that describe 'template' field must be
         rewrited to enclose 'choices' and 'default' options inside a
         function instead of hardcoded values. Else new migration could be
         triggered on any change from settings.

         See initial 'Slider' object migration for a sample.
"""
from django.conf import settings
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from filebrowser.fields import FileBrowseField

from cms.models.pluginmodel import CMSPlugin


def get_template_choices():
    return settings.BLOCKS_SLIDER_TEMPLATES


def get_template_default():
    return settings.BLOCKS_SLIDER_TEMPLATES[0][0]


@python_2_unicode_compatible
class Slider(CMSPlugin):
    """
    Slide container
    """
    title = models.CharField(
        _('title'),
        blank=False,
        max_length=50,
        default="",
    )
    template = models.CharField(
        _('model'),
        blank=True,
        max_length=100,
        choices=get_template_choices(),
        default=get_template_default(),
        help_text=_('Used template for content look.'),
    )

    def __str__(self):
        return self.title

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



@python_2_unicode_compatible
class SlideItem(models.Model):
    """
    Slide item
    """
    slider = models.ForeignKey(
        Slider,
        related_name="slide_item"
    )

    background = models.ImageField(
        _('Background image'),
        upload_to='blocks/slider/%y/%m',
        max_length=255,
        null=True,
        blank=False,
        default=None,
    )
    content = models.TextField(
        _(u"Content"),
        default="",
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

    def __init__(self, *args, **kwargs):
        super(SlideItem, self).__init__(*args, **kwargs)
        self.content = force_text(self.content)

    def __str__(self):
        return Truncator(strip_tags(self.content)).words(4, truncate="...")

    def save(self, *args, **kwargs):
        super(SlideItem, self).save(*args, **kwargs)
