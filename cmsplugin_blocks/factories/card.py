# -*- coding: utf-8 -*-
import random
import factory

from cmsplugin_blocks.choices_helpers import get_card_default_template
from cmsplugin_blocks.utils.factories import create_image_file
from cmsplugin_blocks.models import Card


class CardFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Card.
    """
    template = get_card_default_template()
    content = factory.Faker("text", max_nb_chars=42)

    class Meta:
        model = Card

    @factory.lazy_attribute
    def alignment(self):
        """
        Select a random alignment
        """
        return random.choice([item[0] for item in Card.ALIGNMENT_CHOICES])

    @factory.lazy_attribute
    def image(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()
