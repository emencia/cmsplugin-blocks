# -*- coding: utf-8 -*-
import zipfile

from django.conf import settings
from django.forms import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


def is_valid_image_filename(filename):
    """
    Basic image validation based on its filename.

    Arguments:
        filename (string): File name.

    Returns:
        boolean: True if filename is valid else False.
    """
    ext = filename.split('.')[-1]

    if ext.lower() in settings.BLOCKS_ALLOWED_IMAGE_EXTENSIONS:
        return True

    return False


def validate_file_size(data):
    """
    Validate file size does not exceed limit from
    ``settings.BLOCKS_MASSUPLOAD_FILESIZE_LIMIT``.

    Raises:
        ValidationError: If file size is over limit.

    Arguments:
        data (file object):

    Returns:
        boolean: Always True, obvisously excepted if an exception is raised
        when file is over limit.
    """
    msg = _('Please keep filesize under {}. Current filesize {}')

    # "_size" attribute is only available for Django<2.1, for greater Django
    # version it is "size"
    size = getattr(data, "_size", None) or getattr(data, "size")

    if size > settings.BLOCKS_MASSUPLOAD_FILESIZE_LIMIT:
        raise ValidationError(msg.format(
            filesizeformat(settings.BLOCKS_MASSUPLOAD_FILESIZE_LIMIT),
            filesizeformat(size)
        ))

    return True


def validate_zip(data, obj=None):
    """
    Validate uploaded ZIP archive file.

    If 'obj' is given and valid temporary store it as 'uploaded_zip' attribute
    onto object.

    Raises:
        ValidationError: If not a valid zip file or has corrupted files
            (return corrupted filename in exception).

    Arguments:
        data (file object): A file like object suitable to zipfile module.

    Keyword Arguments:
        obj (object): Optional object where to store temporary archive.

    Returns:
        zipfile.ZipFile: ZIP file object from given path.
    """
    # Validate ZIP from file metas first octets
    if not zipfile.is_zipfile(data):
        raise ValidationError("Submitted file is not a ZIP archive file")

    # Open ZIP
    try:
        archive = zipfile.ZipFile(data)
    except zipfile.BadZipFile:
        raise ValidationError("Submitted ZIP file is invalid")

    # Search for corrupted files
    corrupted_file = archive.testzip()
    if corrupted_file:
        raise ValidationError("File '{}' in ZIP archive is corrupted".format(
            corrupted_file
        ))

    # ZIP is totally ok, store it to attribute
    if obj:
        obj.uploaded_zip = archive

    return archive
