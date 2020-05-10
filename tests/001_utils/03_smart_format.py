import os

import pytest

from tests.utils import get_test_source

from django.core.files.storage import get_storage_class

from cmsplugin_blocks.utils import SmartFormatMixin, SvgFile


class DummyFile:
    """
    Dummy File object just for ``name`` attribute.
    """
    def __init__(self, name):
        self.name = name


@pytest.mark.parametrize("filename,expected", [
    (
        None,
        None,
    ),
    (
        "bar",
        None,
    ),
    (
        "bar.txt",
        None,
    ),
    (
        "bar.jp.txt",
        None,
    ),
    (
        "bar.jpg",
        "JPEG",
    ),
    (
        "bar.jpeg",
        "JPEG",
    ),
    (
        "bar.txt.jpg",
        "JPEG",
    ),
    (
        "bar.png",
        "PNG",
    ),
    (
        "bar.gif",
        "GIF",
    ),
    (
        "bar.svg",
        "SVG",
    ),
])
def test_validate_file_size_success_under(filename, expected):
    """
    media_format method should return the right format name according to file
    extension.
    """
    mixin = SmartFormatMixin()

    dummy = None
    if filename:
        dummy = DummyFile(filename)

    assert expected == mixin.media_format(dummy)


def test_svgfile():
    """
    SvgFile should have "name" attribute, "url" attribute correct values and
    "exists" method correct response.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(
        storage,
        format_name="SVG",
    )
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source)

    svg = SvgFile(image)

    assert svg.name == image.name
    assert svg.exists() == True

    # Ensure url starts like a url and ends with the file name without to test
    # the full url matching
    assert len(svg.url) > 0
    assert svg.url.startswith("/")
    assert svg.url.endswith(image.name)
