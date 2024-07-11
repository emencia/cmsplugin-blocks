from cmsplugin_blocks.factories import CardFactory, FeatureFactory
from cmsplugin_blocks.forms import CardForm
from cmsplugin_blocks.models import Card
from cmsplugin_blocks.utils.tests import build_post_data_from_object


def test_empty(db, settings):
    """
    Form should not be valid with missing required fields.
    """
    form = CardForm({})

    assert form.is_valid() is False
    assert "template" in form.errors
    assert len(form.errors) == 1


def test_success(db, settings):
    """
    Form should be valid with factory datas.
    """
    feature = FeatureFactory(scope="size", plugins=["Card"])
    card = CardFactory(fill_size_features=[feature])

    data = build_post_data_from_object(
        Card,
        card,
        ignore=[
            "id", "cmsplugin", "size_features", "color_features", "extra_features",
        ]
    )
    data["size_features"] = card.size_features.all()

    form = CardForm(data)
    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory, ignore the image to
    # avoid playing with file
    assert instance.template == card.template
    assert instance.size_features.count() == card.size_features.count()
    assert instance.size_features.count() == 1
    assert instance.content == card.content


def test_empty_feature_choices(db, settings):
    """
    When feature choices are empty, form should still continue to work correctly.
    """
    settings.BLOCKS_FEATURE_PLUGINS = []

    card = CardFactory()

    form = CardForm({
        "template": card.template,
        "image": card.image,
        "content": card.content,
    })

    # import json
    # print(json.dumps(excinfo.value.message_dict, indent=4))
    assert form.is_valid() is True
    instance = form.save()

    # Ensure test runned with empty choices
    assert instance.size_features.count() == 0

    # Checked saved values are the same from factory, ignore the image to
    # avoid playing with file
    assert instance.template == card.template
    assert instance.size_features.count() == card.size_features.count()
    assert instance.content == card.content
