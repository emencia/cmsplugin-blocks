from cmsplugin_blocks.factories import HeroFactory
from cmsplugin_blocks.forms import HeroForm


def test_empty(db, settings):
    """
    Form should not be valid with missing required fields.
    """
    form = HeroForm({})

    assert form.is_valid() is False
    assert "template" in form.errors
    assert "content" in form.errors
    assert len(form.errors) == 2


def test_success(db, settings):
    """
    Form should be valid with factory datas.
    """
    hero = HeroFactory()

    form = HeroForm({
        "template": hero.template,
        "features": hero.features,
        "image": hero.image,
        "content": hero.content,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory, ignore the image to
    # avoid playing with file
    assert instance.template == hero.template
    assert instance.features == hero.features
    assert instance.content == hero.content


def test_empty_feature_choices(db, settings):
    """
    When feature choices are empty, form should still continue to work correctly.
    """
    settings.BLOCKS_HERO_FEATURES = []
    hero = HeroFactory()

    form = HeroForm({
        "template": hero.template,
        "features": hero.features,
        "image": hero.image,
        "content": hero.content,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Ensure test runned with empty choices
    assert instance.features == []

    # Checked saved values are the same from factory, ignore the image to
    # avoid playing with file
    assert instance.template == hero.template
    assert instance.features == hero.features
    assert instance.content == hero.content
