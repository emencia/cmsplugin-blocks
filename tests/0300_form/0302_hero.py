from cmsplugin_blocks.factories import HeroFactory, FeatureFactory
from cmsplugin_blocks.forms import HeroForm
from cmsplugin_blocks.models import Hero
from cmsplugin_blocks.utils.tests import build_post_data_from_object


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
    feature = FeatureFactory(scope="size", plugins=["HeroMain"])
    hero = HeroFactory(fill_size_features=[feature])

    data = build_post_data_from_object(
        Hero,
        hero,
        ignore=[
            "id", "cmsplugin", "size_features", "color_features", "extra_features",
        ]
    )
    data["size_features"] = hero.size_features.all()

    form = HeroForm(data)

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory, ignore the image to
    # avoid playing with file
    assert instance.template == hero.template
    assert instance.size_features.count() == hero.size_features.count()
    assert instance.size_features.count() == 1
    assert instance.content == hero.content


def test_empty_feature_choices(db, settings):
    """
    When feature choices are empty, form should still continue to work correctly.
    """
    settings.BLOCKS_FEATURE_PLUGINS = []

    hero = HeroFactory()

    form = HeroForm({
        "template": hero.template,
        "image": hero.image,
        "content": hero.content,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Ensure test runned with empty choices
    assert instance.size_features.count() == 0

    # Checked saved values are the same from factory, ignore the image to
    # avoid playing with file
    assert instance.template == hero.template
    assert instance.size_features.count() == hero.size_features.count()
    assert instance.content == hero.content
