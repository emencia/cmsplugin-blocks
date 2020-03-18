# -*- coding: utf-8 -*-
import random
import factory

from cmsplugin_blocks.choices_helpers import get_album_default_template
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
    image = factory.django.FileField(filename="foo.jpg")

    class Meta:
        model = AlbumItem
