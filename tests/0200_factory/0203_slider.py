from cmsplugin_blocks.choices_helpers import (
    get_slider_feature_choices,
    get_slideritem_feature_choices,
    get_slider_template_default,
)
from cmsplugin_blocks.factories import SliderFactory, SlideItemFactory


def test_slider_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = SliderFactory()
    assert instance.template == get_slider_template_default()

    instance = SliderFactory(template="foo")
    assert instance.template == "foo"

    choices = [v[0] for v in get_slider_feature_choices()]
    assert isinstance(instance.features, list) is True
    assert (instance.features[0] in choices) is True


def test_slider_factory_empty_features(db, settings):
    """
    Factory should behaves correctly when feature choices is empty
    """
    settings.BLOCKS_SLIDER_FEATURES = []

    instance = SliderFactory()

    choices = [v[0] for v in get_slider_feature_choices()]
    assert len(choices) == 0
    assert isinstance(instance.features, list) is True
    assert len(instance.features) == 0


def test_item_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    slider = SliderFactory()

    instance = SlideItemFactory(slider=slider, title="foo")
    assert instance.title == "foo"
    assert instance.slider == slider

    choices = [v[0] for v in get_slideritem_feature_choices()]
    assert isinstance(instance.features, list) is True
    assert (instance.features[0] in choices) is True


def test_item_factory_empty_features(db, settings):
    """
    Factory should behaves correctly when feature choices is empty
    """
    settings.BLOCKS_SLIDERITEM_FEATURES = []

    slider = SliderFactory()

    instance = SlideItemFactory(slider=slider)

    choices = [v[0] for v in get_slideritem_feature_choices()]
    assert len(choices) == 0
    assert isinstance(instance.features, list) is True
    assert len(instance.features) == 0
