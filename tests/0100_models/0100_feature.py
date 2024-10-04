import pytest

from django.core.exceptions import ValidationError

from cmsplugin_blocks.models.feature import Feature


def test_basic(db):
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


def test_value_whitespaces_unallowed(db, settings):
    """
    If setting 'BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES' is false, model validation does
    not accept whitespace in value.
    """
    settings.BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES = False

    instance = Feature(
        title="Foo",
        value="Dummy Yummy",
        scope="size",
        plugins=["Card", "Hero"],
    )
    with pytest.raises(ValidationError):
        instance.full_clean()


def test_value_whitespaces_allowed(db, settings):
    """
    If setting 'BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES' is true, model validation does
    accept whitespace in value.
    """
    settings.BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES = True

    instance = Feature(
        title="Foo",
        value="Dummy Yummy",
        scope="size",
        plugins=["Card", "Hero"],
    )
    instance.full_clean()
    instance.save()

    created = Feature.objects.get(pk=instance.id)

    assert created.value == "Dummy Yummy"


def test_plugins_add(db):
    """
    Demonstrate how to define multiple plugin items on a feature.
    """
    instance = Feature(
        title="Foo",
        value="Dummy",
        scope="size",
        plugins=["Card", "Hero"],
    )
    instance.full_clean()
    instance.save()

    created = Feature.objects.get(pk=instance.id)

    assert created.plugins == ["Card", "Hero"]


def test_plugins_string(db):
    """
    Demonstrate that giving a string as 'plugins' value works only for knowed plugin
    names (from settings), unknowed plugin names are splitted but this should not
    happen since it 'full_clean' should not let them pass choice validation.
    """
    card = Feature(
        title="Carte",
        value="card",
        scope="size",
        plugins="Card",
    )
    card.full_clean()
    card.save()
    created = Feature.objects.get(pk=card.id)
    assert created.plugins == ["Card"]

    foo = Feature(
        title="Foo",
        value="Dummy",
        scope="size",
        plugins="foo",
    )
    # Bypass full_clean for this case
    foo.save()
    created = Feature.objects.get(pk=foo.id)
    assert created.plugins == ["f", "o", "o"]
