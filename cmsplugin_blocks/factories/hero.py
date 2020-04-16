# -*- coding: utf-8 -*-
import factory

from cmsplugin_blocks.choices_helpers import get_hero_default_template
from cmsplugin_blocks.utils.factories import create_image_file
from cmsplugin_blocks.models import Hero


class HeroFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Hero.
    """
    template = get_hero_default_template()
    content = factory.Faker("text", max_nb_chars=42)

    class Meta:
        model = Hero

    @factory.lazy_attribute
    def image(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()
