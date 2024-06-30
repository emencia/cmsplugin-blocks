"""
A container component with a title, image, features, content and able to include other
plugins.
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

from ..choices_helpers import (
    get_container_feature_choices,
    get_container_template_choices,
    get_container_template_default,
)
from ..modelfields import CommaSeparatedStringsField
from ..utils.validators import validate_css_classnames


class Container(SmartFormatMixin, CMSPlugin):
    """
    Container component.
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
        choices=get_container_template_choices(),
        default=get_container_template_default(),
        help_text=_("Used template for content look."),
    )
    """
    Template choice from available plugin templates in setting
    ``BLOCKS_CONTAINER_TEMPLATES``. Default to the first choice item.
    """

    image = SmartMediaField(
        _("Image"),
        max_length=255,
        blank=True,
        null=True,
        default=None,
        upload_to="blocks/container/%y/%m",
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
    Required long text, it will be editable through CKeditor on plugin form.
    """

    features = CommaSeparatedStringsField(
        _("Layout features"),
        choices=get_container_feature_choices(),
        blank=True,
        default="",
        max_length=255,
        validators=[validate_css_classnames],
    )
    """
    Optional string of CSS class names divided by a single comma.
    """

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

    def get_features(self):
        """
        Merge feature items into a string with a space divider.

        Returns:
            string: Feature items divided by a comma. Duplicate items are removed
            and original order is preserved.
        """
        return " ".join(
            list(dict.fromkeys(self.features))
        )

    class Meta:
        verbose_name = _("Container")
        verbose_name_plural = _("Containers")


pre_save.connect(
    auto_purge_files_on_change(["image"]),
    dispatch_uid="block_container_files_on_change",
    sender=Container,
    weak=False,
)
