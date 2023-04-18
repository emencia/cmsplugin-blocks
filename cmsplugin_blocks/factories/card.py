import random

import factory
import faker

from ..choices_helpers import (
    get_card_feature_choices,
    get_card_template_default,
)
from ..utils.factories import create_image_file
from ..models import Card


class CardFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Card.
    """
    title = factory.Faker("text", max_nb_chars=20)
    template = get_card_template_default()
    content = factory.Faker("text", max_nb_chars=42)
    link_open_blank = factory.Faker("pybool")

    class Meta:
        model = Card

    @factory.lazy_attribute
    def features(self):
        """
        Build features value with an item from feature choices.

        If there is no feature choices available, just return an empty string.
        """
        choices = get_card_feature_choices()

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

    @factory.lazy_attribute
    def link_url(self):
        """
        Set a random url
        """
        Faker = faker.Faker()
        return Faker.url()
