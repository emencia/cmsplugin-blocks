import random

import factory

from ..choices_helpers import (
    get_album_feature_choices,
    get_albumitem_feature_choices,
    get_album_template_default,
)
from ..utils.factories import create_image_file
from ..models import Album, AlbumItem


class AlbumFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Album.
    """
    template = get_album_template_default()
    title = factory.Faker("text", max_nb_chars=20)

    @factory.lazy_attribute
    def features(self):
        """
        Build features value with an item from feature choices.

        If there is no feature choices available, just return an empty string.
        """
        choices = get_album_feature_choices()

        if not choices:
            return []

        return [random.choice(choices)[0]]

    class Meta:
        model = Album


class AlbumItemFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a AlbumItem.
    """
    album = factory.SubFactory(AlbumFactory)
    title = factory.Faker("text", max_nb_chars=20)
    order = factory.Sequence(lambda n: 10 * n)
    image_alt = factory.Faker("text", max_nb_chars=10)

    class Meta:
        model = AlbumItem

    @factory.lazy_attribute
    def features(self):
        """
        Build features value with an item from feature choices.

        If there is no feature choices available, just return an empty string.
        """
        choices = get_albumitem_feature_choices()

        if not choices:
            return []

        return [random.choice(choices)[0]]

    @factory.lazy_attribute
    def image(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()
