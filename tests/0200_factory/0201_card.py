from cmsplugin_blocks.choices_helpers import (
    get_card_feature_choices,
    get_card_template_default,
)
from cmsplugin_blocks.factories import CardFactory


def test_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = CardFactory()
    assert instance.template == get_card_template_default()

    instance = CardFactory(template="foo")
    assert instance.template == "foo"

    choices = [v[0] for v in get_card_feature_choices()]
    assert isinstance(instance.features, list) is True
    assert (instance.features[0] in choices) is True


def test_factory_empty_features(db, settings):
    """
    Factory should behaves correctly when feature choices is empty
    """
    settings.BLOCKS_CARD_FEATURES = []

    instance = CardFactory()

    choices = [v[0] for v in get_card_feature_choices()]
    assert len(choices) == 0
    assert isinstance(instance.features, list) is True
    assert len(instance.features) == 0
