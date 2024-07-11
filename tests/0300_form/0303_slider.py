from cmsplugin_blocks.factories import SliderFactory, SlideItemFactory, FeatureFactory
from cmsplugin_blocks.forms import SliderForm, SlideItemForm
from cmsplugin_blocks.utils.tests import build_post_data_from_object
from cmsplugin_blocks.models import Slider


def test_slider_empty(db, client, settings):
    """
    Container form should not be valid with missing required fields.
    """
    form = SliderForm({})

    assert form.is_valid() is False
    assert "title" in form.errors
    assert "template" in form.errors
    assert len(form.errors) == 2


def test_item_empty(db, client, settings):
    """
    Item form should not be valid with missing required fields.
    """
    form = SlideItemForm({})

    assert form.is_valid() is False
    assert "slider" in form.errors
    assert "title" in form.errors
    assert "order" in form.errors
    assert "image" in form.errors
    assert len(form.errors) == 4


def test_slider_success(db, client, settings):
    """
    Form should be valid with factory datas.
    """
    feature = FeatureFactory(scope="size", plugins=["Slider"])
    slider = SliderFactory(fill_size_features=[feature])

    data = build_post_data_from_object(
        Slider,
        slider,
        ignore=[
            "id", "cmsplugin", "size_features", "color_features", "extra_features",
        ]
    )
    data["size_features"] = slider.size_features.all()

    form = SliderForm(data)

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory
    assert instance.title == slider.title
    assert instance.size_features.count() == slider.size_features.count()
    assert instance.size_features.count() == 1
    assert instance.template == slider.template


def test_slider_empty_feature_choices(db, client, settings):
    """
    When feature choices are empty, form should still continue to work correctly.
    """
    settings.BLOCKS_FEATURE_PLUGINS = []

    slider = SliderFactory()

    form = SliderForm({
        "title": slider.title,
        "template": slider.template,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Ensure test runned with empty choices
    assert instance.size_features.count() == 0

    # Checked saved values are the same from factory
    assert instance.title == slider.title
    assert instance.size_features.count() == slider.size_features.count()
    assert instance.template == slider.template


def test_item_success(db, client, settings):
    """
    Item form should be valid with factory datas.
    """
    slider = SliderFactory()
    item = SlideItemFactory(slider=slider)

    form = SlideItemForm({
        "slider": item.slider,
        "title": item.title,
        "order": item.order,
    }, {
        "image": item.image,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory
    assert instance.slider == slider
    assert instance.order == item.order
    assert instance.image == item.image
