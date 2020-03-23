import io
import os
import zipfile

import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from cmsplugin_blocks.utils import store_images_from_zip, validate_zip


class DummyContainer:
    """
    A dummy container object to store temporary ZIP file.
    """
    pass


class DummyFileField:
    """
    A dummy FileField object to lazily mock it.

    Only the required methods from ``store_images_from_zip`` workflow are
    softly implemented.
    """
    def __init__(self, *args, **kwargs):
        self.filename = None
        self.data = None

    def save(self, filename, data, save=None):
        self.filename = filename
        self.data = data

        return filename


class DummyAlbum:
    """
    A dummy Album object to lazily mock an Album model.

    Only the required methods from ``store_images_from_zip`` workflow are
    softly implemented.
    """
    def __init__(self, title):
        self.title = title

    def save(self, *args, **kwargs):
        pass


class DummyItem:
    """
    A dummy Item object to lazily mock an AlbumItem model.

    Only the required methods from ``store_images_from_zip`` workflow are
    softly implemented.
    """
    def __init__(self, album=None):
        self.album = album
        self.image = DummyFileField()
        self.title = None


@pytest.mark.parametrize("filename,expected_items", [
    (
        "basic.zip",
        [
            "basic/107x107.png",
            "basic/120x100.jpg",
            "basic/120x100.png",
            "basic/120x120.png",
        ],
    ),
    (
        "include_non_image_files.zip",
        [
            'include_non_image_files/107x107.png',
            'include_non_image_files/120x100.jpg',
            'include_non_image_files/120x100.png',
            'include_non_image_files/120x120.png',
        ]
    ),
    (
        "with_subdirectories.zip",
        [
            'with_subdirectories/107x107.png',
            'with_subdirectories/120x100.jpg',
            'with_subdirectories/subdir/120x100.png',
            'with_subdirectories/subdir/120x120.png',
        ],
    ),
])
def test_store_images_from_zip_success(caplog, testsettings, filename,
                                       expected_items):
    """
    "store_images_from_zip" should find every images from given ZIP file and
    store it into AlbumItem items which should be linked to given Album
    instance.
    """
    filepath = os.path.join(
        testsettings.fixtures_path,
        "zip_samples",
        filename
    )

    # Open file as a ZIP and attach it to dummy container instance
    container = DummyContainer()
    validate_zip(filepath, obj=container)

    assert isinstance(container.uploaded_zip, zipfile.ZipFile)
    assert filepath == container.uploaded_zip.filename

    # Make a dummy album
    album = DummyAlbum(title=filename)

    # Collect image file from ZIP file
    album._awaiting_items = store_images_from_zip(
        album,
        container.uploaded_zip,
        DummyItem,
        'album',
        'image',
        label_attrname="title"
    )

    #print(caplog.record_tuples)
    errors = [msg for name,level,msg in caplog.record_tuples if (name == "cmsplugin_blocks.utils")]

    assert 0 == len(errors)

    # Validate 'album' relation is equal to 'album' instance
    for item in album._awaiting_items:
        assert item.album == album

    # Build expected items with a tuple (title, image_filename) for each
    # expected item. The title is identical to the filename.
    expected_items = [(item, item) for item in expected_items]

    # Build a list of found items to compare against "expected_items"
    found_items = [(item.title, item.image.filename) for item in album._awaiting_items]

    assert expected_items == found_items
