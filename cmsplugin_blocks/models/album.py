"""
An album component you may use in a gallery.

Album items are ordered from their ``order`` field value. Items with a zero
value for their order will be ordered in an almost arbitrary order (mostly
depending from item object id).

Album form have a special field ``mass_upload``, it expects a valid ZIP archive
file to create items. Archive file is limited to the value from setting
``BLOCKS_MASSUPLOAD_FILESIZE_LIMIT``.

The archive file may contains one or many image files with enabled format from
django-smart-media setting ``SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS``. Each image will
create a new Album item where the name will be filled with the full relative image file
path. Images in archive can be structured in multiple subdirectory. Created Album item
from an archive don't have any order.
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

from ..choices_helpers import get_album_template_choices, get_album_template_default
from .mixins import FeatureMixinModel


class Album(FeatureMixinModel, CMSPlugin):
    """
    Album container for items.
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
        choices=get_album_template_choices(),
        default=get_album_template_default(),
        help_text=_("Used template for content formatting."),
    )
    """
    Template choice from available plugin templates in setting
    ``BLOCKS_ALBUM_TEMPLATES``. Default to the first choice item.
    """

    size_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("size features"),
        related_name="%(app_label)s_%(class)s_size_related",
        blank=True,
        limit_choices_to={"scope": "size", "plugins__contains": "Album"},
    )
    """
    Optional related size features.
    """

    color_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("color features"),
        related_name="%(app_label)s_%(class)s_color_related",
        blank=True,
        limit_choices_to={"scope": "color", "plugins__contains": "Album"},
    )
    """
    Optional related color features.
    """

    extra_features = models.ManyToManyField(
        "cmsplugin_blocks.Feature",
        verbose_name=_("extra features"),
        related_name="%(app_label)s_%(class)s_extra_related",
        blank=True,
        limit_choices_to={"scope": "extra", "plugins__contains": "Album"},
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
        Copy all relations when plugin object is copied as another object.

        See:

        https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html#relations-between-plugins
        """
        super().copy_relations(oldinstance)

        self.album_item.all().delete()

        for album_item in oldinstance.album_item.all():
            album_item.pk = None
            album_item.album = self
            album_item.save()

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")


class AlbumItem(SmartFormatMixin, models.Model):
    """
    Album item to include in container.
    """
    album = models.ForeignKey(
        Album,
        related_name="album_item",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        _("Title"),
        blank=True,
        max_length=150,
        default="",
    )
    """
    Optional title string.
    """

    order = models.IntegerField(
        _("Order"),
        blank=False,
        default=0
    )
    """
    Number for order position in item list.
    """

    image = SmartMediaField(
        _("Image"),
        max_length=255,
        null=True,
        blank=False,
        default=None,
        upload_to="blocks/albumitem/%y/%m",
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

    def __str__(self):
        return Truncator(strip_tags(self.title)).words(
            settings.BLOCKS_MODEL_TRUNCATION_LENGTH,
            truncate=settings.BLOCKS_MODEL_TRUNCATION_CHR
        )

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = _("Album item")
        verbose_name_plural = _("Album items")


pre_save.connect(
    auto_purge_files_on_change(["image"]),
    dispatch_uid="block_albumitem_files_on_change",
    sender=AlbumItem,
    weak=False,
)
