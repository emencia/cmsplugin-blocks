from cmsplugin_blocks.choices_helpers import get_feature_plugin_choices
from cmsplugin_blocks.factories import FeatureFactory


def test_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = FeatureFactory()
    assert len(instance.title) > 0
    assert len(instance.value) > 0
    assert len(instance.scope) > 0
    assert len(instance.plugins) > 0
    instance.full_clean()

    choices = [v[0] for v in get_feature_plugin_choices()]
    assert isinstance(instance.plugins, list) is True
    assert (instance.plugins[0] in choices) is True


def test_factory_empty_features(db, settings):
    """
    Factory should behaves correctly when feature choices is empty
    """
    settings.BLOCKS_FEATURE_PLUGINS = []

    instance = FeatureFactory()

    choices = [v[0] for v in get_feature_plugin_choices()]
    assert len(choices) == 0
    assert isinstance(instance.plugins, list) is True
    assert len(instance.plugins) == 0
