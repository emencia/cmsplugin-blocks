import zipfile

from django.conf import settings
from django.core.exceptions import ValidationError
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
    ext = filename.split(".")[-1]

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
    msg = _("Please keep filesize under {}. Current filesize {}")

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


def validate_css_classname(value):
    """
    A callable validator to validate a CSS class name.

    A value is assumed to be a valid CSS class name if:

    * Is not empty;
    * Does not start with a number;
    * Only contains alphanumeric characters, ``_`` or ``-``;

    Raises:
        ValidationError: If given value is an invalid CSS class name.

    Arguments:
        value (string): A string with a CSS class name to validate.

    Returns:
        bool: True if valid.

    """
    msg = _("'%(value)s' is not a valid CSS class name")

    if not value:
        raise ValidationError(msg, params={"value": value})

    for i, item in enumerate(value):
        if i == 0 and item.isdigit():
            raise ValidationError(msg, params={"value": value})

        if item.isalnum() or item in ["-", "_"]:
            continue

        raise ValidationError(msg, params={"value": value})

    return True


def validate_css_classnames(value):
    """
    A callable validator to validate a list of CSS class names using
    ``validate_css_classname`` on each item.

    Raises:
        ValidationError: If an item is an invalid CSS class name.

    Arguments:
        value (list): A list of strings for CSS class names to validate.

    Returns:
        bool: True if every list item are valid.

    """
    for item in value:
        validate_css_classname(item)

    return True
