import pytest

from cmsplugin_blocks.choices_helpers import get_slider_default_template
from cmsplugin_blocks.factories.slider import SliderFactory, SlideItemFactory


def test_slider_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = SliderFactory()
    assert instance.template == get_slider_default_template()

    instance = SliderFactory(template="foo")
    assert instance.template == "foo"


def test_item_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    slider = SliderFactory()

    item = SlideItemFactory(slider=slider, title="foo")
    assert item.title == "foo"
    assert item.slider == slider
