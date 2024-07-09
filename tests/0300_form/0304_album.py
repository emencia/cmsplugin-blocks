import io
import os

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from cmsplugin_blocks.models import Album
from cmsplugin_blocks.factories import AlbumFactory, AlbumItemFactory, FeatureFactory
from cmsplugin_blocks.forms import AlbumForm, AlbumItemForm
from cmsplugin_blocks.utils.tests import build_post_data_from_object


def test_album_empty(db, client, tests_settings, settings):
    """
    Container form should not be valid with missing required fields.
    """
    form = AlbumForm({})

    assert form.is_valid() is False
    assert "title" in form.errors
    assert "template" in form.errors
    assert len(form.errors) == 2


def test_item_empty(db, client, tests_settings, settings):
    """
    Item form should not be valid with missing required fields.
    """
    form = AlbumItemForm({})

    assert form.is_valid() is False
    assert "album" in form.errors
    assert "order" in form.errors
    assert "image" in form.errors
    assert len(form.errors) == 3


def test_album_success(db, client, tests_settings, settings):
    """
    Form should be valid with factory datas.
    """
    feature = FeatureFactory(scope="size", plugins=["AlbumMain"])
    album = AlbumFactory(fill_size_features=[feature])

    data = build_post_data_from_object(
        Album,
        album,
        ignore=[
            "id", "cmsplugin", "size_features", "color_features", "extra_features",
        ]
    )
    data["size_features"] = album.size_features.all()
    form = AlbumForm(data)

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory
    assert instance.title == album.title
    assert instance.size_features.count() == album.size_features.count()
    assert instance.size_features.count() == 1
    assert instance.template == album.template


def test_album_empty_feature_choices(db, client, tests_settings, settings):
    """
    When feature choices are empty, form should still continue to work correctly.
    """
    settings.BLOCKS_FEATURE_PLUGINS = []

    album = AlbumFactory()

    form = AlbumForm({
        "title": album.title,
        "template": album.template,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Ensure test runned with empty choices
    assert instance.size_features.count() == 0

    # Checked saved values are the same from factory
    assert instance.title == album.title
    assert instance.size_features.count() == album.size_features.count()
    assert instance.template == album.template


def test_item_success(db, client, tests_settings, settings):
    """
    Item form should be valid with factory datas.
    """
    album = AlbumFactory()
    item = AlbumItemFactory(album=album)

    form = AlbumItemForm({
        "album": item.album,
        "order": item.order,
    }, {
        "image": item.image,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Checked saved values are the same from factory
    assert instance.album == album
    assert instance.order == item.order
    assert instance.image == item.image


def test_mass_upload_success(db, client, tests_settings, settings):
    """
    When "mass_upload" field is filled with a valid ZIP file, form save
    should fill the Album attribute ``_awaiting_items`` with AlbumItem
    instances for each valid image file from ZIP archive.
    """
    album = AlbumFactory()

    filepath = os.path.join(
        tests_settings.fixtures_path,
        "zip_samples",
        "basic.zip"
    )

    with io.open(filepath, "rb") as fp:
        _archive = SimpleUploadedFile(
            "basic.zip",
            fp.read(),
            content_type="application/zip"
        )

    form = AlbumForm({
        "title": album.title,
        "template": album.template,
    }, {
        "mass_upload": _archive,
    })

    assert form.is_valid() is True
    instance = form.save()

    # Expected item counter
    assert len(instance._awaiting_items) == 4

    # Check expected item without image file since saved file path may
    # contain a random hash we don't know yet
    def item_matrix(v):
        return {
            "id": v.id,
            "title": v.title,
            "order": 0,
        }

    result_items = [item_matrix(item) for item in instance._awaiting_items]
    expected_items = [
        {"id": None, "title": "basic/107x107.png", "order": 0},
        {"id": None, "title": "basic/120x100.jpg", "order": 0},
        {"id": None, "title": "basic/120x100.png", "order": 0},
        {"id": None, "title": "basic/120x120.png", "order": 0},
    ]

    assert result_items == expected_items

    # For sanity check the image file attribute is not empty and is an
    # image file (simply assumed from file extension)
    for item in instance._awaiting_items:
        assert item.image is not None
        assert (item.image.url.endswith(".jpg") or item.image.url.endswith(".png"))


def test_mass_upload_fail(db, client, tests_settings, settings):
    """
    When "mass_upload" field is filled with an invalid ZIP file, form error
    should be present about invalid field and an exception should be raised
    when trying to save.
    """
    album = AlbumFactory()

    filepath = os.path.join(
        tests_settings.fixtures_path,
        "zip_samples",
        "truncated.zip"
    )

    with io.open(filepath, "rb") as fp:
        _archive = SimpleUploadedFile(
            "truncated.zip",
            fp.read(),
            content_type="application/zip"
        )

    form = AlbumForm({
        "title": album.title,
        "template": album.template,
    }, {
        "mass_upload": _archive,
    })

    assert form.is_valid() is False
    assert "mass_upload" in form.errors
    assert len(form.errors) == 1

    with pytest.raises(ValueError):
        form.save()
