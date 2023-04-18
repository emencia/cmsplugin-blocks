"""
A hero component with an image (commonly for background) and a content.
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.encoding import force_str
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from smart_media.mixins import SmartFormatMixin
from smart_media.modelfields import SmartMediaField
from smart_media.signals import auto_purge_files_on_change, auto_purge_files_on_delete

from ..choices_helpers import (
    get_hero_feature_choices,
    get_hero_template_choices,
    get_hero_template_default,
)
from ..modelfields import CommaSeparatedStringsField
from ..utils.validators import validate_css_classnames


class Hero(SmartFormatMixin, CMSPlugin):
    """
    Hero component.
    """
    template = models.CharField(
        _("Template"),
        blank=False,
        max_length=150,
        choices=get_hero_template_choices(),
        default=get_hero_template_default(),
        help_text=_("Used template for content look."),
    )
    """
    Template choice from available plugin templates in setting
    ``BLOCKS_HERO_TEMPLATES``. Default to the first choice item.
    """

    features = CommaSeparatedStringsField(
        _("Layout features"),
        choices=get_hero_feature_choices(),
        blank=True,
        default="",
        max_length=255,
        validators=[validate_css_classnames],
    )
    """
    Optional string of CSS class names divided by a single comma.
    """

    image = SmartMediaField(
        _("Image"),
        max_length=255,
        blank=True,
        null=True,
        default=None,
        upload_to="blocks/hero/%y/%m",
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
        self.content = force_str(self.content)

    def __str__(self):
        return Truncator(strip_tags(self.content)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def get_features(self):
        """
        Merge feature items into a string with a comma divider.

        Returns:
            string: Feature items divided by a comma. Duplicate items are removed
            and original order is preserved.
        """
        return " ".join(
            list(dict.fromkeys(self.features))
        )

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = _("Hero")
        verbose_name_plural = _("Heros")


post_delete.connect(
    auto_purge_files_on_delete(["image"]),
    dispatch_uid="block_hero_files_on_delete",
    sender=Hero,
    weak=False,
)
pre_save.connect(
    auto_purge_files_on_change(["image"]),
    dispatch_uid="block_hero_files_on_change",
    sender=Hero,
    weak=False,
)
