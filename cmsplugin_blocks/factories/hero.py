import factory

from ..choices_helpers import get_hero_template_default
from ..utils.factories import create_image_file
from ..models import Hero

from .feature import FeatureFactory


class HeroFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Hero.
    """
    template = get_hero_template_default()
    content = factory.Faker("text", max_nb_chars=42)
    image_alt = factory.Faker("text", max_nb_chars=10)

    class Meta:
        model = Hero
        skip_postgeneration_save = True

    @factory.lazy_attribute
    def image(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()

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
        # Do nothing for build strategy
        if not create or not extracted:
            return []

        # Create a new random feature
        if extracted is True:
            features = [FeatureFactory(scope="size", plugins=["HeroMain"])]
        # Take given feature objects
        else:
            features = extracted

        # Add features
        for feature in features:
            self.size_features.add(feature)

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
        # Do nothing for build strategy
        if not create or not extracted:
            return []

        # Create a new random feature
        if extracted is True:
            features = [FeatureFactory(scope="color", plugins=["HeroMain"])]
        # Take given feature objects
        else:
            features = extracted

        # Add features
        for feature in features:
            self.color_features.add(feature)

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
        # Do nothing for build strategy
        if not create or not extracted:
            return []

        # Create a new random feature
        if extracted is True:
            features = [FeatureFactory(scope="extra", plugins=["HeroMain"])]
        # Take given feature objects
        else:
            features = extracted

        # Add features
        for feature in features:
            self.extra_features.add(feature)
