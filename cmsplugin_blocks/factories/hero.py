# -*- coding: utf-8 -*-
import factory

from cmsplugin_blocks.choices_helpers import get_hero_default_template
from cmsplugin_blocks.models import Hero


class HeroFactory(factory.django.DjangoModelFactory):
    """
    Factory to create random instances of Hero for testing.
    """

    class Meta:
        model = Hero

    template = get_hero_default_template()
    content = factory.Faker("text", max_nb_chars=42)
    #image = factory.django.FileField(filename='foo.jpg')
    image = factory.django.ImageField(color='blue')
