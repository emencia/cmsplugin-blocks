# -*- coding: utf-8 -*-
import random
import factory

from cmsplugin_blocks.choices_helpers import get_slider_default_template
from cmsplugin_blocks.utils.factories import create_image_file
from cmsplugin_blocks.models import Slider, SlideItem


class SliderFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Slider.
    """
    template = get_slider_default_template()
    title = factory.Faker("text", max_nb_chars=20)

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

    class Meta:
        model = SlideItem

    @factory.lazy_attribute
    def link_url(self):
        """
        Set a random url or nothing, randomly
        """
        trigger = random.choice([True, False])

        if trigger:
            return factory.Faker("url").generate({})

        return ""

    @factory.lazy_attribute
    def image(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()
