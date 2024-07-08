from cmsplugin_blocks.factories import ContainerFactory
from cmsplugin_blocks.forms import ContainerForm


def test_empty(db):
    """
    Form should not be valid with missing required fields.
    """
    form = ContainerForm({})

    assert form.is_valid() is False
    assert "template" in form.errors
    assert len(form.errors) == 1


def test_success(db):
    """
    Form should be valid with factory datas.
    """
    container = ContainerFactory()

    form = ContainerForm({
        "template": container.template,
        "image": container.image,
        "content": container.content,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory, ignore the image to
    # avoid playing with file
    assert instance.template == container.template
    assert instance.content == container.content


def test_empty_feature_choices(db, settings):
    """
    When feature choices are empty, form should still continue to work correctly.
    """
    settings.BLOCKS_FEATURE_PLUGINS = []

    container = ContainerFactory()

    form = ContainerForm({
        "template": container.template,
        "image": container.image,
        "content": container.content,
    })

    # import json
    # print(json.dumps(excinfo.value.message_dict, indent=4))
    assert form.is_valid() is True
    instance = form.save()

    # Ensure test runned with empty choices
    assert instance.size_features.count() == 0

    # Checked saved values are the same from factory, ignore the image to
    # avoid playing with file
    assert instance.template == container.template
    assert instance.size_features.count() == container.size_features.count()
    assert instance.content == container.content
