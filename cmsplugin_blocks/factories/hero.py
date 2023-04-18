import random

import factory

from ..choices_helpers import (
    get_hero_feature_choices,
    get_hero_template_default,
)
from ..utils.factories import create_image_file
from ..models import Hero


class HeroFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Hero.
    """
    template = get_hero_template_default()
    content = factory.Faker("text", max_nb_chars=42)

    class Meta:
        model = Hero

    @factory.lazy_attribute
    def features(self):
        """
        Build features value with an item from feature choices.

        If there is no feature choices available, just return an empty string.
        """
        choices = get_hero_feature_choices()

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
