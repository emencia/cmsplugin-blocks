import factory

from ..choices_helpers import get_album_template_default
from ..utils.factories import create_image_file
from ..models import Album, AlbumItem

from .feature import fill_scope_features


class AlbumFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Album.
    """
    template = get_album_template_default()
    title = factory.Faker("text", max_nb_chars=20)

    class Meta:
        model = Album
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
            ["Album"],
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
            ["Album"],
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
            ["Album"],
            create,
            extracted,
            **kwargs
        )


class AlbumItemFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a AlbumItem.
    """
    album = factory.SubFactory(AlbumFactory)
    title = factory.Faker("text", max_nb_chars=20)
    order = factory.Sequence(lambda n: 10 * n)
    image_alt = factory.Faker("text", max_nb_chars=10)

    class Meta:
        model = AlbumItem

    @factory.lazy_attribute
    def image(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()
