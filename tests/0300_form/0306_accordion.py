from cmsplugin_blocks.factories import (
    AccordionFactory, AccordionItemFactory, FeatureFactory
)
from cmsplugin_blocks.forms import AccordionForm, AccordionItemForm
from cmsplugin_blocks.utils.tests import build_post_data_from_object
from cmsplugin_blocks.models import Accordion


def test_accordion_empty(db, client, settings):
    """
    Container form should not be valid with missing required fields.
    """
    form = AccordionForm({})

    assert form.is_valid() is False
    assert "title" in form.errors
    assert "template" in form.errors
    assert len(form.errors) == 2


def test_item_empty(db, client, settings):
    """
    Item form should not be valid with missing required fields.
    """
    form = AccordionItemForm({})

    assert form.is_valid() is False
    assert "accordion" in form.errors
    assert "title" in form.errors
    assert "order" in form.errors
    assert "image" in form.errors
    assert len(form.errors) == 4


def test_accordion_success(db, client, settings):
    """
    Form should be valid with factory datas.
    """
    feature = FeatureFactory(scope="size", plugins=["Accordion"])
    accordion = AccordionFactory(fill_size_features=[feature])

    data = build_post_data_from_object(
        Accordion,
        accordion,
        ignore=[
            "id", "cmsplugin", "size_features", "color_features", "extra_features",
        ]
    )
    data["size_features"] = accordion.size_features.all()

    form = AccordionForm(data)

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory
    assert instance.title == accordion.title
    assert instance.size_features.count() == accordion.size_features.count()
    assert instance.size_features.count() == 1
    assert instance.template == accordion.template


def test_accordion_empty_feature_choices(db, client, settings):
    """
    When feature choices are empty, form should still continue to work correctly.
    """
    settings.BLOCKS_FEATURE_PLUGINS = []

    accordion = AccordionFactory()

    form = AccordionForm({
        "title": accordion.title,
        "template": accordion.template,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Ensure test runned with empty choices
    assert instance.size_features.count() == 0

    # Checked saved values are the same from factory
    assert instance.title == accordion.title
    assert instance.size_features.count() == accordion.size_features.count()
    assert instance.template == accordion.template


def test_item_success(db, client, settings):
    """
    Item form should be valid with factory datas.
    """
    accordion = AccordionFactory()
    item = AccordionItemFactory(accordion=accordion)

    form = AccordionItemForm({
        "accordion": item.accordion,
        "title": item.title,
        "order": item.order,
    }, {
        "image": item.image,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory
    assert instance.accordion == accordion
    assert instance.order == item.order
    assert instance.image == item.image
