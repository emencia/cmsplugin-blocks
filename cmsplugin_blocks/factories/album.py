# -*- coding: utf-8 -*-
import factory

from cmsplugin_blocks.choices_helpers import get_album_default_template
from cmsplugin_blocks.utils.factories import create_image_file
from cmsplugin_blocks.models import Album, AlbumItem


class AlbumFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Album.
    """
    template = get_album_default_template()
    title = factory.Faker("text", max_nb_chars=20)

    class Meta:
        model = Album


class AlbumItemFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a AlbumItem.
    """
    album = factory.SubFactory(AlbumFactory)
    title = factory.Faker("text", max_nb_chars=20)
    order = factory.Sequence(lambda n: 10 * n)

    class Meta:
        model = AlbumItem

    @factory.lazy_attribute
    def image(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()
