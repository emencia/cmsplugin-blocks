import io
from pathlib import Path

from PIL import Image

from cmsplugin_blocks.compat.default_storage import DEFAULT_STORAGE
from cmsplugin_blocks.utils.factories import create_image_file


def test_create_image_file_basic():
    """
    Basic usage without arguments should succeed with a created file as
    expected from default argument values.
    """
    image = create_image_file()

    destination = Path("pil") / image.name

    assert image.name == "blue.png"

    DEFAULT_STORAGE.save(destination, image)
    saved = DEFAULT_STORAGE.path(destination)

    assert Path(saved).exists() is True

    try:
        with Image.open(saved) as im:
            # Since image are just single plain color we can pick any pixel to
            # verify expected color
            pixel_sample = im.getpixel((10, 10))

            assert im.format == "PNG"
            assert im.size == (100, 100)
            assert pixel_sample == (0, 0, 255, 255)
    except IOError:
        print("Cannot open image file with PIL:", saved)
        raise


def test_create_image_file_args():
    """
    Should succeed with a created file as expected from given arguments.
    """
    image = create_image_file(
        filename="foo.red",
        size=(200, 200),
        color="red",
        format_name="PNG"
    )

    destination = Path("pil") / image.name

    assert image.name == "foo.red"

    DEFAULT_STORAGE.save(destination, image)
    saved = DEFAULT_STORAGE.path(destination)

    assert Path(saved).exists() is True

    try:
        with Image.open(saved) as im:
            # Since image are just single plain color we can pick any pixel to
            # verify expected color
            pixel_sample = im.getpixel((10, 10))

            assert im.format == "PNG"
            assert im.size == (200, 200)
            assert pixel_sample == (255, 0, 0, 255)
    except IOError:
        print("Cannot open image file with PIL:", saved)
        raise


def test_create_image_file_jpg():
    """
    Created image should be in the required format from argument.
    """
    image = create_image_file(
        format_name="JPEG"
    )

    destination = Path("pil") / image.name

    assert image.name == "blue.jpg"

    DEFAULT_STORAGE.save(destination, image)
    saved = DEFAULT_STORAGE.path(destination)

    assert Path(saved).exists() is True

    try:
        with Image.open(saved) as im:
            assert im.format == "JPEG"
    except IOError:
        print("Cannot open image file with PIL:", saved)
        raise


def test_create_image_file_gif():
    """
    Created image should be in the required format from argument.
    """
    image = create_image_file(
        format_name="GIF"
    )

    destination = Path("pil") / image.name

    assert image.name == "blue.gif"

    DEFAULT_STORAGE.save(destination, image)
    saved = DEFAULT_STORAGE.path(destination)

    assert Path(saved).exists() is True

    try:
        with Image.open(saved) as im:
            assert im.format == "GIF"
    except IOError:
        print("Cannot open image file with PIL:", saved)
        raise


def test_create_image_file_svg():
    """
    SVG format should create a dummy SVG file.
    """
    image = create_image_file(
        format_name="SVG",
        color="green",
        size=(150, 80),
    )

    destination = Path("pil") / image.name

    assert image.name == "green.svg"

    DEFAULT_STORAGE.save(destination, image)
    saved = DEFAULT_STORAGE.path(destination)

    assert Path(saved).exists() is True

    with io.open(saved) as fp:
        content = fp.read()

    expected = (
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 80">"""
        """<path fill="green" d="M0 0h150v80H0z"/>"""
        """</svg>"""
    )

    assert content == expected
