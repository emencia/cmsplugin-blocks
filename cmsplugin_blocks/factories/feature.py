import random

import factory

from django.utils.text import slugify

from ..choices_helpers import get_feature_plugin_choices
from ..models import Feature


class FeatureFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Feature.
    """
    title = factory.Sequence(lambda n: "Feature {0}".format(n))

    class Meta:
        model = Feature

    @factory.lazy_attribute
    def value(self):
        """
        Slugify title to make a dummy but valid css classname value.

        .. Warning::
            This is not totally safe with some non alphanumeric characters in custom
            title. However the default title from factory will always be safe.
        """
        return slugify(self.title)

    @factory.lazy_attribute
    def scope(self):
        """
        Use a random scope value
        """
        return random.choice(Feature.SCOPE_CHOICES)[0]

    @factory.lazy_attribute
    def plugins(self):
        """
        Use a random plugins value
        """
        choices = get_feature_plugin_choices()
        return [] if not choices else [random.choice(choices)[0]]
