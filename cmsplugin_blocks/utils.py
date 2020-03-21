# -*- coding: utf-8 -*-
import collections
import zipfile

from io import BytesIO

# For Python 2/3 support
try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

from django.conf import settings
from django.forms import ValidationError
from django.template.defaultfilters import filesizeformat
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _


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

    if data._size > settings.BLOCKS_MASSUPLOAD_FILESIZE_LIMIT:
        raise ValidationError(msg.format(
            filesizeformat(settings.BLOCKS_MASSUPLOAD_FILESIZE_LIMIT),
            filesizeformat(data._size)
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


def store_images_from_zip(instance, zip_fileobject, item_model,
                          link_attrname, image_attrname,
                          label_attrname=None):
    """
    Collect every image from a ZIP as an item object linked to given
    saved instance.

    Once image searching is finished the zip file object is closed.

    This does not really save any item object to deal with 'creation' state
    from instance that does not have an id yet. Items are created and stored
    in a list of item to save further.

    Arguments:
        instance (object): Saved instance to link to item objects.
        zip_fileobject (zipfile.ZipFile): A valid zip file object to search
            for images.
        item_model (model): Model object used to create items objects.
        link_attrname (string): Attribute name used for linking instance to
            item object. This must relate to a Foreign key field.
        image_attrname (string): Attribute name used to store image file in
            item object. This must relate to a FileField or an ImageField
            field.

    Keyword Arguments:
        label_attrname (string): Optional attribute name to fill with image
            filename. If given it must relate to a CharField or a TextField
            field. If CharField, it should have enough character limit to
            accept long paths.

    Returns:
        list: List of saved objects from image items.
    """
    stored_items = []

    if zip_fileobject:
        for filename in sorted(zip_fileobject.namelist()):
            # Don't process invalid filename or directory
            if filename.endswith('/') or \
                not is_valid_image_filename(filename):
                continue

            # Get archived file from ZIP
            data = zip_fileobject.read(filename)
            if len(data):
                try:
                    # the following is taken from
                    # django.forms.fields.ImageField: load() could spot a
                    # truncated JPEG, but it loads the entire image in memory,
                    # which is a DoS vector. See #3848 and #18520. verify()
                    # must be called immediately after the constructor.
                    PILImage.open(BytesIO(data)).verify()
                except Exception as e:
                    # if a "bad" file is found we just skip it.
                    print('Error verifying image: {}'.format(str(e)))
                    continue

                if hasattr(data, 'seek') and isinstance(data.seek,
                                                        collections.Callable):
                    print('seeked')
                    data.seek(0)

                try:
                    item = item_model(**{link_attrname:instance})
                    # Lazy save since we dont have album id yet when creating
                    getattr(item, image_attrname).save(filename,
                                                       ContentFile(data),
                                                       save=False)

                    # Optional string field to fill from filename
                    if label_attrname:
                        setattr(item, label_attrname, filename)
                except Exception as e:
                    print('Error creating item from file: {}'.format(str(e)))
                else:
                    # Store created item to be saved further in plugin
                    # 'save_model' method
                    stored_items.append(item)

        # Drop ZIP file object from memory/tempdir when finished
        zip_fileobject.close()

    return stored_items


class SmartFormatMixin(object):
    """
    A mixin to inherit from a model so it will have some common helper
    methods to manage image formats.
    """
    def media_format(self, mediafile):
        """
        Common method to perform a naive check about image format using file
        extension.

        This has been done for common image formats, so it will return either
        'JPEG', 'PNG', 'SVG' or None if it does not match any of these formats.

        Obviously, since it use the file extension, found format is not to be
        100% trusted. For sanity, media saving should validate it correclty
        and possibly enforce the right file extension according to file format
        found from file metas (like with the PIL method to get it).

        At least the FileField should validate than uploaded file is a valid
        image.

        Why using this naive technique ? To be able to use it in templates
        without cache and so avoid to open image file each time template
        is rendered.

        Arguments:
            mediafile (object): Either a FileField or ImageField or any other
                object which implement a ``name`` attribute which return the
                filename.

        Return:
            string: Format name if filename extension match to any available
            format extension, else ``None``.
        """
        if mediafile:
            ext = mediafile.name.split(".")[-1].lower()
            if ext in ["jpg", "jpeg"]:
                return "JPEG"
            elif ext in ["png"]:
                return "PNG"
            elif ext in ["gif"]:
                return "GIF"
            elif ext in ["svg"]:
                return "SVG"

        return None
