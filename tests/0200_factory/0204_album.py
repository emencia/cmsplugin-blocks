from cmsplugin_blocks.choices_helpers import (
    get_album_feature_choices,
    get_albumitem_feature_choices,
    get_album_template_default,
)
from cmsplugin_blocks.factories import AlbumFactory, AlbumItemFactory


def test_album_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = AlbumFactory()
    assert instance.template == get_album_template_default()

    instance = AlbumFactory(template="foo")
    assert instance.template == "foo"

    choices = [v[0] for v in get_album_feature_choices()]
    assert isinstance(instance.features, list) is True
    assert (instance.features[0] in choices) is True


def test_album_factory_empty_features(db, settings):
    """
    Factory should behaves correctly when feature choices is empty
    """
    settings.BLOCKS_ALBUM_FEATURES = []

    instance = AlbumFactory()

    choices = [v[0] for v in get_album_feature_choices()]
    assert len(choices) == 0
    assert isinstance(instance.features, list) is True
    assert len(instance.features) == 0


def test_item_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    album = AlbumFactory()

    instance = AlbumItemFactory(album=album, title="foo")
    assert instance.title == "foo"
    assert instance.album == album

    choices = [v[0] for v in get_albumitem_feature_choices()]
    assert isinstance(instance.features, list) is True
    assert (instance.features[0] in choices) is True


def test_item_factory_empty_features(db, settings):
    """
    Factory should behaves correctly when feature choices is empty
    """
    settings.BLOCKS_ALBUMITEM_FEATURES = []

    album = AlbumFactory()

    instance = AlbumItemFactory(album=album)

    choices = [v[0] for v in get_albumitem_feature_choices()]
    assert len(choices) == 0
    assert isinstance(instance.features, list) is True
    assert len(instance.features) == 0
