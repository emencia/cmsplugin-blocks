from cmsplugin_blocks.choices_helpers import get_card_template_default
from cmsplugin_blocks.factories import CardFactory, FeatureFactory


def test_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = CardFactory()
    instance.full_clean()
    assert instance.template == get_card_template_default()

    instance = CardFactory(content="foo")
    instance.full_clean()
    assert instance.content == "foo"


def test_feature_getters(db):
    """
    Features getters should return the right features with scope and plugins enforced.
    """
    size_foo = FeatureFactory(title="Foo", scope="size", plugins=["Card"])
    size_bar = FeatureFactory(title="Bar", scope="size", plugins=[
        "Album",
        "Card"
    ])
    color_foo = FeatureFactory(title="Foo", scope="color", plugins=["Card"])
    color_zap = FeatureFactory(title="Zap", scope="color", plugins=["Album"])
    color_ping = FeatureFactory(title="Ping", scope="color", plugins=[
        "Card",
        "Hero"
    ])
    extra_bang = FeatureFactory(title="bang", scope="extra", plugins=["Card"])

    first_card = CardFactory(
        fill_size_features=[size_foo, size_bar],
        fill_color_features=[color_ping, color_foo, color_zap],
    )
    first_card.full_clean()
    assert first_card.scoped_features() == {
        "color": ["foo", "ping"],
        "extra": [],
        "size": ["bar", "foo"],
    }
    assert first_card.flat_features() == "bar foo ping"

    second_card = CardFactory(
        fill_size_features=[size_foo, color_foo],
        fill_color_features=[color_ping, color_foo, color_zap],
        fill_extra_features=[size_foo, color_zap, extra_bang],
    )
    second_card.full_clean()
    assert second_card.scoped_features() == {
        "color": ["foo", "ping"],
        "extra": ["bang"],
        "size": ["foo"],
    }
    assert second_card.flat_features() == "bang foo ping"
