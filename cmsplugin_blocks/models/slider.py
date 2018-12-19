# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from cmsplugin_blocks.choices_helpers import (get_slider_default_template,
                                              get_slider_template_choices)

@python_2_unicode_compatible
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

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')


@python_2_unicode_compatible
class SlideItem(models.Model):
    """
    Slide item
    """
    slider = models.ForeignKey(
        Slider,
        related_name="slide_item"
    )

    image = models.ImageField(
        _('Image'),
        upload_to='blocks/slider/%y/%m',
        max_length=255,
        null=True,
        blank=False,
        default=None,
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

    def __init__(self, *args, **kwargs):
        super(SlideItem, self).__init__(*args, **kwargs)
        self.content = force_text(self.content)

    def __str__(self):
        return Truncator(strip_tags(self.content)).words(4, truncate="...")

    class Meta:
        verbose_name = _('Slide item')
        verbose_name_plural = _('Slide items')
