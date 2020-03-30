import pytest

from django.conf import settings

from tests.utils import get_fake_words

from cmsplugin_blocks.models.album import Album, AlbumItem


def test_basic(db, settings):
    """
    Basic model saving with required fields should not fail
    """
    album = Album(
        title="Foo",
        template="Dummy"
    )
    album.save()

    assert 1 == Album.objects.filter(title="Foo").count()
    assert "Foo" == album.title

    item = AlbumItem(
        album=album,
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert 1 == AlbumItem.objects.filter(image="ping.jpg").count()
    assert 42 == item.order
    assert album == item.album
    assert [item] == list(album.album_item.all())


def test_str_truncation_under_limit(db, settings):
    """
    Model str should be equal to saved string when under the limit.
    """
    title = get_fake_words(length=settings.BLOCKS_MODEL_TRUNCATION_LENGTH)
    album = Album(
        title=title,
        template="Dummy"
    )
    album.save()

    assert title == str(album)

    title = get_fake_words(length=settings.BLOCKS_MODEL_TRUNCATION_LENGTH)
    item = AlbumItem(
        album=album,
        title=title,
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert title == str(item)


def test_str_truncation_over_limit(db, settings):
    """
    Model str should be truncated to X words when over the limit from setting
    ``BLOCKS_MODEL_TRUNCATION_LENGTH``.
    """
    limit = settings.BLOCKS_MODEL_TRUNCATION_LENGTH + 3

    title = get_fake_words(length=limit)
    album = Album(
        title=title,
        template="Dummy"
    )
    album.save()

    assert len(title) > len(str(album))
    assert str(album).endswith(settings.BLOCKS_MODEL_TRUNCATION_CHR)

    title = get_fake_words(length=limit)
    item = AlbumItem(
        album=album,
        title=title,
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert len(title) > len(str(item))
    assert str(item).endswith(settings.BLOCKS_MODEL_TRUNCATION_CHR)


def test_str_strip_tags(db, settings):
    """
    Model str should be cleaned from any HTML tags and unicode character are
    not broken.
    """
    album = Album(
        title="<p>Foo 日本</p>",
        template="Dummy"
    )
    album.save()

    assert "<p>Foo 日本</p>" == album.title
    assert "Foo 日本" == str(album)

    item = AlbumItem(
        album=album,
        title="<p>Ping 日本</p>",
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert "<p>Ping 日本</p>" == item.title
    assert "Ping 日本" == str(item)


def test_item_image_format(db, settings):
    """
    Method to get image format should return a valid value without any error.
    """
    album = Album(
        title="Foo",
        template="Dummy"
    )
    album.save()

    item = AlbumItem(
        album=album,
        order=42,
        image="foo.jpg",
    )
    item.save()

    assert item.get_image_format() == "JPEG"
