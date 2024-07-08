from cmsplugin_blocks.choices_helpers import get_album_template_default
from cmsplugin_blocks.factories import AlbumFactory, AlbumItemFactory


def test_album_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = AlbumFactory()
    assert instance.template == get_album_template_default()

    instance = AlbumFactory(template="foo")
    assert instance.template == "foo"


def test_item_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    album = AlbumFactory()

    instance = AlbumItemFactory(album=album, title="foo")
    assert instance.title == "foo"
    assert instance.album == album
