# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class EstablishmentOpening(CMSPlugin):
    """
    Container for opening days
    """
    title = models.CharField(
        _('title'),
        blank=False,
        max_length=50,
        default="",
    )
    comment = models.TextField(
        _(u"comment"),
        blank=True,
        default="",
    )

    def __str__(self):
        return self.title

    def copy_relations(self, oldinstance):
        """
        Copy FK relations when plugin object is copied as another object

        See:

        http://docs.django-cms.org/en/latest/how_to/custom_plugins.html#for-foreign-key-relations-from-other-objects
        """
        self.day_item.all().delete()

        for day_item in oldinstance.day_item.all():
            day_item.pk = None
            day_item.opening = self
            day_item.save()

    class Meta:
        verbose_name = _('Establishment opening')
        verbose_name_plural = _('Establishment openings')


@python_2_unicode_compatible
class DayItem(models.Model):
    """
    Day item
    """
    opening = models.ForeignKey(
        EstablishmentOpening,
        related_name="day_item"
    )

    name = models.CharField(
        _('name'),
        blank=False,
        max_length=50,
        default="",
    )
    hours = models.TextField(
        _(u"Hours"),
        blank=False,
        default="",
    )

    def __init__(self, *args, **kwargs):
        super(DayItem, self).__init__(*args, **kwargs)
        self.hours = force_text(self.hours)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Opening day item')
        verbose_name_plural = _('Opening days items')
