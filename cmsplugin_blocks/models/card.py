"""
A card component with a title, image, features and content.
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils.encoding import force_str
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from smart_media.mixins import SmartFormatMixin
from smart_media.modelfields import SmartMediaField
from smart_media.signals import auto_purge_files_on_change

from ..choices_helpers import get_card_template_choices, get_card_template_default
from .mixins import FeatureMixinModel


class Card(SmartFormatMixin, FeatureMixinModel, CMSPlugin):
    """
    Card component.
    """

    title = models.CharField(
        _("Title"),
        blank=True,
        max_length=150,
        default="",
    )
    """
    An optional title string.
    """

    template = models.CharField(
        _("Template"),
        blank=False,
        max_length=150,
        choices=get_card_template_choices(),
        default=get_card_template_default(),
        help_text=_("Used template for content look."),
    )
    """
    Template choice from available plugin templates in setting
    ``BLOCKS_CARD_TEMPLATES``. Default to the first choice item.
    """

    image = SmartMediaField(
        _("Image"),
        max_length=255,
        blank=True,
        null=True,
        default=None,
        upload_to="blocks/card/%y/%m",
    )
    """
    Optional image file, limited to enabled image formats from settings
    ``BLOCKS_ALLOWED_IMAGE_EXTENSIONS``.
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
        _("Content"),
        blank=True,
        default="",
    )
    """
    Optional long text, it will be editable through CKeditor on plugin form.
    """

    link_url = models.CharField(
        _("Link url"),
        blank=True,
        max_length=255,
    )
    """
    Optional string for link URL.
    """

    link_open_blank = models.BooleanField(
        _("Open in new window"),
        default=False,
        help_text=_("If checked the link will be opened in a new window"),
    )
    """
    Checkbox to enable opening link URL in a new window/tab.
    """

    size_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("size features"),
        related_name="%(app_label)s_%(class)s_size_related",
        blank=True,
        limit_choices_to={"scope": "size", "plugins__contains": "CardMain"},
    )
    """
    Optional related size features.
    """

    color_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("color features"),
        related_name="%(app_label)s_%(class)s_color_related",
        blank=True,
        limit_choices_to={"scope": "color", "plugins__contains": "CardMain"},
    )
    """
    Optional related color features.
    """

    extra_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("extra features"),
        related_name="%(app_label)s_%(class)s_extra_related",
        blank=True,
        limit_choices_to={"scope": "extra", "plugins__contains": "CardMain"},
    )
    """
    Optional related extra features.
    """

    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = force_str(self.content)

    def __str__(self):
        return Truncator(strip_tags(self.content)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def get_image_format(self):
        return self.media_format(self.image)


pre_save.connect(
    auto_purge_files_on_change(["image"]),
    dispatch_uid="block_card_files_on_change",
    sender=Card,
    weak=False,
)
