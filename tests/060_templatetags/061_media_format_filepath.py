import io
import os

from PIL import Image

import pytest

from tests.utils import get_test_source

from django.core.files.storage import get_storage_class
from django.template import Context, Template

from cmsplugin_blocks.exceptions import (
    InvalidFormatError, IncompatibleSvgToBitmap, IncompatibleBitmapToSvg
)


def test_basic(db):
    """
    Basic usage should create a thumb with default format and expected size
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(storage)
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source) == True

    # Template to use tag with dummy image
    t = Template(
        (
            "{% load smart_format %}"
            "{% media_format_url myfileobject geometry %}"
        )
    )
    # Template context to pass tag arguments
    c = {
        "myfileobject": image,
        "geometry": "50x50",
    }

    # Render template with tag usage
    result = t.render(Context(c))
    thumb_filepath = storage.path(result.strip())

    # Fail because the File object given to sorl have the initial required file
    # name which is not the final filename (which have additional unique hash)
    assert os.path.exists(thumb_filepath) == True

    # Open created image file with PIL for validation
    with Image.open(thumb_filepath) as im:
        assert im.format == "PNG"
        assert im.size == (50, 50)


def test_upscale_disabled(db):
    """
    Usage "upscale" option to False should not upscale a source smaller than
    required geometry.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(storage, size=(50, 50))
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source) == True

    # Template to use tag with dummy image
    t = Template(
        (
            "{% load smart_format %}"
            "{% media_format_url myfileobject geometry upscale=upscale %}"
        )
    )
    # Template context to pass tag arguments
    c = {
        "myfileobject": image,
        "geometry": "100x100",
        "upscale": False,
    }

    # Render template with tag usage
    result = t.render(Context(c))
    thumb_filepath = storage.path(result.strip())

    # Fail because the File object given to sorl have the initial required file
    # name which is not the final filename (which have additional unique hash)
    assert os.path.exists(thumb_filepath) == True

    # Open created image file with PIL for validation
    with Image.open(thumb_filepath) as im:
        assert im.format == "PNG"
        # Original source size is respected
        assert im.size == (50, 50)


@pytest.mark.parametrize("expected", [
    "JPEG",
    "PNG",
    "GIF",
])
def test_format_auto_bitmap(db, expected):
    """
    Default auto format for a Bitmap should use the same format than source.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(
        storage,
        format_name=expected,
    )
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source) == True

    # Template to use tag with dummy image
    t = Template(
        (
            "{% load smart_format %}"
            "{% media_format_url myfileobject geometry %}"
        )
    )
    # Template context to pass tag arguments
    c = {
        "myfileobject": image,
        "geometry": "50x50",
    }

    # Render template with tag usage
    result = t.render(Context(c))
    thumb_filepath = storage.path(result.strip())

    assert os.path.exists(thumb_filepath) == True

    # Open created image file with PIL for validation
    with Image.open(thumb_filepath) as im:
        assert im.format == expected


def test_format_auto_svg(db):
    """
    Automatic format for SVG should be correctly detected and just return the
    source since we don't create thumb for this format.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(
        storage,
        format_name="SVG",
    )
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source) == True

    # Template to use tag with dummy image
    t = Template(
        (
            "{% load smart_format %}"
            "{% media_format_url myfileobject geometry %}"
        )
    )
    # Template context to pass tag arguments
    c = {
        "myfileobject": image,
        "geometry": "50x50",
    }

    # Render template with tag usage
    result = t.render(Context(c))
    thumb_filepath = storage.path(result.strip())

    assert os.path.exists(thumb_filepath) == True

    # Thumb object is the source file object
    assert thumb_filepath == saved_source

    # Ensure this is a svg file
    with io.open(thumb_filepath, "r") as fp:
        content = fp.read()

    assert content.startswith("<svg") == True


def test_format_invalid_format_name(db):
    """
    When given format name is not supported, it should raise an exception.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(
        storage,
        format_name="PNG",
    )
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source) == True

    # Template to use tag with dummy image
    t = Template(
        (
            "{% load smart_format %}"
            "{% media_format_url myfileobject geometry format=format %}"
        )
    )
    # Template context to pass tag arguments
    c = {
        "myfileobject": image,
        "geometry": "50x50",
        "format": "NOPE",
    }

    # Render template with tag usage
    with pytest.raises(InvalidFormatError):
        result = t.render(Context(c))


def test_format_forced_jpeg(db):
    """
    When a specific Bitmap format is given, it should be respected no matter
    the source format is.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(
        storage,
        format_name="PNG",
    )
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source) == True

    # Template to use tag with dummy image
    t = Template(
        (
            "{% load smart_format %}"
            "{% media_format_url myfileobject geometry format=format %}"
        )
    )
    # Template context to pass tag arguments
    c = {
        "myfileobject": image,
        "geometry": "50x50",
        "format": "JPEG",
    }

    # Render template with tag usage
    result = t.render(Context(c))
    thumb_filepath = storage.path(result.strip())

    assert os.path.exists(thumb_filepath) == True

    # Open created image file with PIL for validation
    with Image.open(thumb_filepath) as im:
        assert im.format == "JPEG"


def test_format_incompatible_bitmap_to_svg(db):
    """
    When required format is SVG for a Bitmap source, it should raise an
    exception since PIL is not able to create SVG.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(
        storage,
        format_name="PNG",
    )
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source) == True

    # Template to use tag with dummy image
    t = Template(
        (
            "{% load smart_format %}"
            "{% media_format_url myfileobject geometry format=format %}"
        )
    )
    # Template context to pass tag arguments
    c = {
        "myfileobject": image,
        "geometry": "50x50",
        "format": "SVG",
    }

    # Render template with tag usage
    with pytest.raises(IncompatibleBitmapToSvg):
        result = t.render(Context(c))


def test_format_incompatible_svg_to_bitmap(db):
    """
    When required format is a Bitmap for a SVG source, it should raise an
    exception since PIL is not able to read SVG.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(
        storage,
        format_name="SVG",
    )
    saved_source = storage.path(image.name)

    assert os.path.exists(saved_source) == True

    # Template to use tag with dummy image
    t = Template(
        (
            "{% load smart_format %}"
            "{% media_format_url myfileobject geometry format=format %}"
        )
    )
    # Template context to pass tag arguments
    c = {
        "myfileobject": image,
        "geometry": "50x50",
        "format": "PNG",
    }

    # Render template with tag usage
    with pytest.raises(IncompatibleSvgToBitmap):
        result = t.render(Context(c))
