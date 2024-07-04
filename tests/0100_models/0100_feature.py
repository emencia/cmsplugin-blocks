import pytest

from django.core.exceptions import ValidationError

from cmsplugin_blocks.models.feature import Feature


def test_basic(db, settings):
    """
    Basic model saving with required fields should not fail
    """
    instance = Feature(
        title="Foo",
        value="Dummy",
        scope="size",
    )
    instance.full_clean()
    instance.save()

    created = Feature.objects.get(pk=instance.id)

    assert 1 == Feature.objects.filter(title="Foo").count()
    assert created.title == "Foo"
    assert created.plugins == []


def test_model_required_fields(db):
    """
    Basic model validation with missing required fields should fail.
    """
    instance = Feature()

    with pytest.raises(ValidationError) as excinfo:
        instance.full_clean()

    # import json
    # print(json.dumps(excinfo.value.message_dict, indent=4))
    assert excinfo.value.message_dict == {
        "title": [
            "This field cannot be blank."
        ],
        "value": [
            "This field cannot be blank."
        ]
    }


def test_plugins_add(db, settings):
    """
    Demonstrate how to add multiple feature items
    """
    instance = Feature(
        title="Foo",
        value="Dummy",
        scope="size",
        plugins=["foo", "bar"],
    )
    instance.save()

    created = Feature.objects.get(pk=instance.id)

    assert ["foo", "bar"] == created.plugins


def test_plugins_wrong(db, settings):
    """
    Demonstrate that giving a string to feature does not work as it could be expected.
    """
    instance = Feature(
        title="Foo",
        value="Dummy",
        scope="size",
        plugins="foo",
    )
    instance.save()

    created = Feature.objects.get(pk=instance.id)

    assert ["f", "o", "o"] == created.plugins
