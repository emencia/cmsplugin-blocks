import random

import factory

from django.conf import settings
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


def fill_scope_features(instance, scope, plugins, create, extracted, **kwargs):
    """
    Add features to a model which use Feature relations as described in
    ``cmsplugin_blocks.models.mixins.FeatureMixinModel``.

    Arguments:
        instance (Model): Model instance where to push features.
        scope (string): Scope to use when creating random features. This is used
            when Feature objects to add are directly given. And also it is needed
            to build the model field attribute where the items are added (like
            ``size_features``).
        plugins (list): List of plugin names to use when creating random features.
            This is not used when Feature objects to add are directly given.
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
        features = [FeatureFactory(scope=scope, plugins=plugins)]
    # Take given feature objects
    else:
        features = extracted

    # Add features
    for feature in features:
        # Checking given scope and plugin names for sanity since factory bypasses
        # model cleaning validation
        assert feature.scope in [k for k, v in Feature.SCOPE_CHOICES]
        assert len([
            name
            for name in feature.plugins
            if name not in settings.BLOCKS_KNOWED_FEATURES_PLUGINS
        ]) == 0

        fieldname = "{}_features".format(scope)
        getattr(instance, fieldname).add(feature)
