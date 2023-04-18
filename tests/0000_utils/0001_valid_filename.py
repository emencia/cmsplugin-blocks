import pytest

from cmsplugin_blocks.utils import is_valid_image_filename


@pytest.mark.parametrize("filename,expected", [
    (
        "/foo/bar",
        False,
    ),
    (
        "bar.txt",
        False,
    ),
    (
        "bar.jpg.txt",
        False,
    ),
    (
        "bar.txt",
        False,
    ),
    (
        "bar.jpg",
        True,
    ),
    (
        "/foo/bar.jpg",
        True,
    ),
    (
        "/foo/bar.txt.jpg",
        True,
    ),
    (
        "bar.png",
        True,
    ),
    (
        "bar.gif",
        True,
    ),
    (
        "bar.svg",
        True,
    ),
])
def test_is_valid_image_filename(filename, expected):
    """

    """
    assert expected == is_valid_image_filename(filename)
