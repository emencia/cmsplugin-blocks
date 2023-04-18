import os
import zipfile

import pytest

from django.core.exceptions import ValidationError

from cmsplugin_blocks.utils import validate_zip


class Dummy:
    """
    A dummy object to receive ``uploaded_zip`` attribute from validate_zip.
    """
    pass


@pytest.mark.parametrize("filename", [
    "foo.txt",
    "image_faked_as_zip_archive.zip",
])
def test_validate_zip_not_a_zip(tests_settings, filename):
    """
    An exception should be raised when file is not a ZIP file.
    """
    filepath = os.path.join(
        tests_settings.fixtures_path,
        "zip_samples",
        filename
    )

    with pytest.raises(ValidationError):
        validate_zip(filepath)


def test_validate_zip_invalid(tests_settings):
    """
    An exception should be raised when ZIP file is invalid.
    """
    filepath = os.path.join(
        tests_settings.fixtures_path,
        "zip_samples",
        "truncated.zip",
    )

    with pytest.raises(ValidationError):
        validate_zip(filepath)


@pytest.mark.parametrize("filename", [
    "basic.zip",
    "include_non_image_files.zip",
    "with_subdirectories.zip",
])
def test_validate_zip(tests_settings, filename):
    """
    For a basic valid ZIP file, validation should return a ``zipfile.ZipFile``
    object.
    """
    filepath = os.path.join(
        tests_settings.fixtures_path,
        "zip_samples",
        filename
    )

    archive = validate_zip(filepath)

    assert isinstance(archive, zipfile.ZipFile)
    assert filepath == archive.filename


def test_valid_zip_basic_to_object(tests_settings):
    """
    Successful validation should attach valid ZipFile to ``uploaded_zip``
    attribute on given object in argument ``obj``.
    """
    filepath = os.path.join(
        tests_settings.fixtures_path,
        "zip_samples",
        "basic.zip"
    )

    dummy = Dummy()

    validate_zip(filepath, obj=dummy)

    assert isinstance(dummy.uploaded_zip, zipfile.ZipFile)
    assert filepath == dummy.uploaded_zip.filename
