import factory
import faker

from ..choices_helpers import get_slider_template_default
from ..utils.factories import create_image_file
from ..models import Slider, SlideItem

from .feature import fill_scope_features


class SliderFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Slider.
    """
    template = get_slider_template_default()
    title = factory.Faker("text", max_nb_chars=20)

    class Meta:
        model = Slider
        skip_postgeneration_save = True

    @factory.post_generation
    def fill_size_features(self, create, extracted, **kwargs):
        """
        Add size features.

        Arguments:
            create (bool): True for create strategy, False for build strategy.
            extracted (object): If ``True``, will add a new random feature
                object. If a list assume it's a list of Author objects to add.
                Else if empty don't do anything.
        """
        return fill_scope_features(
            self,
            "size",
            ["Slider"],
            create,
            extracted,
            **kwargs
        )

    @factory.post_generation
    def fill_color_features(self, create, extracted, **kwargs):
        """
        Add color features.

        Arguments:
            create (bool): True for create strategy, False for build strategy.
            extracted (object): If ``True``, will add a new random feature
                object. If a list assume it's a list of Author objects to add.
                Else if empty don't do anything.
        """
        return fill_scope_features(
            self,
            "color",
            ["Slider"],
            create,
            extracted,
            **kwargs
        )

    @factory.post_generation
    def fill_extra_features(self, create, extracted, **kwargs):
        """
        Add extra features.

        Arguments:
            create (bool): True for create strategy, False for build strategy.
            extracted (object): If ``True``, will add a new random feature
                object. If a list assume it's a list of Author objects to add.
                Else if empty don't do anything.
        """
        return fill_scope_features(
            self,
            "extra",
            ["Slider"],
            create,
            extracted,
            **kwargs
        )


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
