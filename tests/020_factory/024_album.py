import pytest

from cmsplugin_blocks.choices_helpers import get_album_default_template
from cmsplugin_blocks.factories.album import AlbumFactory, AlbumItemFactory


def test_album_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = AlbumFactory()
    assert instance.template == get_album_default_template()

    instance = AlbumFactory(template="foo")
    assert instance.template == "foo"


def test_item_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    album = AlbumFactory()

    item = AlbumItemFactory(album=album, title="foo")
    assert item.title == "foo"
    assert item.album == album
