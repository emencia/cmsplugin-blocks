import factory
import faker

from ..choices_helpers import get_card_template_default
from ..utils.factories import create_image_file
from ..models import Card

from .feature import fill_scope_features


class CardFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Card.
    """
    title = factory.Faker("text", max_nb_chars=20)
    template = get_card_template_default()
    content = factory.Faker("text", max_nb_chars=42)
    link_name = factory.Faker("text", max_nb_chars=10)
    link_open_blank = factory.Faker("pybool")
    image_alt = factory.Faker("text", max_nb_chars=10)

    class Meta:
        model = Card
        skip_postgeneration_save = True

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
            ["Card"],
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
            ["Card"],
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
            ["Card"],
            create,
            extracted,
            **kwargs
        )
