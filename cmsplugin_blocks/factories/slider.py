import random

import factory
import faker

from ..choices_helpers import (
    get_slider_feature_choices,
    get_slideritem_feature_choices,
    get_slider_template_default,
)
from ..utils.factories import create_image_file
from ..models import Slider, SlideItem


class SliderFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Slider.
    """
    template = get_slider_template_default()
    title = factory.Faker("text", max_nb_chars=20)

    @factory.lazy_attribute
    def features(self):
        """
        Build features value with an item from feature choices.

        If there is no feature choices available, just return an empty string.
        """
        choices = get_slider_feature_choices()

        if not choices:
            return []

        return [random.choice(choices)[0]]

    class Meta:
        model = Slider


class SlideItemFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a SlideItem.
    """
    slider = factory.SubFactory(SliderFactory)
    title = factory.Faker("text", max_nb_chars=20)
    content = factory.Faker("text", max_nb_chars=42)
    order = factory.Sequence(lambda n: 10 * n)
    link_name = factory.Faker("text", max_nb_chars=10)
    link_open_blank = factory.Faker("pybool")
    image_alt = factory.Faker("text", max_nb_chars=10)

    class Meta:
        model = SlideItem

    @factory.lazy_attribute
    def features(self):
        """
        Build features value with an item from feature choices.

        If there is no feature choices available, just return an empty string.
        """
        choices = get_slideritem_feature_choices()

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
