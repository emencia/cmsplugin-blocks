import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from cmsplugin_blocks.utils import validate_file_size


class DummyFile:
    """
    Dummy File object just for ``size`` attribute.
    """
    def __init__(self, size):
        # '_size' was used in Django<=2.1
        self._size = self.size = size


def test_validate_file_size_success_under():
    """
    There should be no error when file size is under limit.
    """
    assert validate_file_size(
        DummyFile(50)
    ) is True


def test_validate_file_size_success_equal():
    """
    There should be no error when file size is equal to the limit.
    """
    assert validate_file_size(
        DummyFile(settings.BLOCKS_MASSUPLOAD_FILESIZE_LIMIT)
    ) is True


def test_validate_file_size_fail():
    """
    An exception should be raised when file is over the limit.
    """
    with pytest.raises(ValidationError):
        validate_file_size(
            DummyFile(settings.BLOCKS_MASSUPLOAD_FILESIZE_LIMIT+1)
        )
