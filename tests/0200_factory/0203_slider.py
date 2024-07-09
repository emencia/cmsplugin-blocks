from cmsplugin_blocks.choices_helpers import get_slider_template_default
from cmsplugin_blocks.factories import SliderFactory, SlideItemFactory


def test_slider_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = SliderFactory()
    assert instance.template == get_slider_template_default()

    instance = SliderFactory(template="foo")
    assert instance.template == "foo"


def test_item_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    slider = SliderFactory()

    instance = SlideItemFactory(slider=slider, title="foo")
    assert instance.title == "foo"
    assert instance.slider == slider
