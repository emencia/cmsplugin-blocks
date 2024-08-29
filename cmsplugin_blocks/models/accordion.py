"""
Represents a accordion component, functionally similar to a Slider, except that
a accordion item cannot contain hyperlinks or their associated contents.

Accordion items are ordered from their ``order`` field value. Items with a zero
value for their order will be ordered in an almost arbitrary order (mostly
depending from item object id).
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from smart_media.mixins import SmartFormatMixin
from smart_media.modelfields import SmartMediaField
from smart_media.signals import auto_purge_files_on_change

from ..choices_helpers import (
    get_accordion_template_choices, get_accordion_template_default
)
from .mixins import FeatureMixinModel


class Accordion(FeatureMixinModel, CMSPlugin):
    """
    Accordion container for items.
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
        choices=get_accordion_template_choices(),
        default=get_accordion_template_default(),
        help_text=_("Used template for content look."),
    )
    """
    Template choice from available plugin templates in setting
    ``BLOCKS_ACCORDION_TEMPLATES``. Default to the first choice item.
    """

    keep_open = models.BooleanField(
        _("Keep items opened"),
        default=False,
        help_text=_(
            "When enabled, the already opened items are not closed when opening other "
            "items. On defaut, once an item is opened all other items are closed."
        ),
    )
    """
    Checkbox to enable "keep items opened" behavior.
    """

    size_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("size features"),
        related_name="%(app_label)s_%(class)s_size_related",
        blank=True,
        limit_choices_to={"scope": "size", "plugins__contains": "Accordion"},
    )
    """
    Optional related size features.
    """

    color_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("color features"),
        related_name="%(app_label)s_%(class)s_color_related",
        blank=True,
        limit_choices_to={"scope": "color", "plugins__contains": "Accordion"},
    )
    """
    Optional related color features.
    """

    extra_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("extra features"),
        related_name="%(app_label)s_%(class)s_extra_related",
        blank=True,
        limit_choices_to={"scope": "extra", "plugins__contains": "Accordion"},
    )
    """
    Optional related extra features.
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
        """
        super().copy_relations(oldinstance)

        self.accordion_item.all().delete()

        for accordion_item in oldinstance.accordion_item.all():
            accordion_item.pk = None
            accordion_item.accordion = self
            accordion_item.save()

    class Meta:
        verbose_name = _("Accordion")
        verbose_name_plural = _("Accordions")


class AccordionItem(SmartFormatMixin, models.Model):
    """
    Accordion item to include in container.
    """
    accordion = models.ForeignKey(
        Accordion,
        related_name="accordion_item",
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

    image = SmartMediaField(
        _("Image"),
        max_length=255,
        null=True,
        blank=True,
        upload_to="blocks/accordionitem/%y/%m",
    )
    """
    Required image file.
    """

    image_alt = models.CharField(
        _("Alternative image text"),
        blank=True,
        max_length=125,
        default="",
    )
    """
    An optional text string for alternative image text.
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

    opened = models.BooleanField(
        _("Initially opened"),
        default=False,
        help_text=_(
            "On default all accordion item are closed and need to be opened manually."
            "This option enables this item to be initially opened."
        ),
    )
    """
    Checkbox to initially open item.
    """

    def __str__(self):
        return Truncator(strip_tags(self.title)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = _("Accordion item")
        verbose_name_plural = _("Accordion items")


pre_save.connect(
    auto_purge_files_on_change(["image"]),
    dispatch_uid="block_accordionitem_files_on_change",
    sender=AccordionItem,
    weak=False,
)
