import collections
import logging

from io import BytesIO

from PIL import Image as PILimage

from django.core.files.base import ContentFile

from .validators import is_valid_image_filename


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

    Since this is a method to be used inside save() method, it is required to
    be silent for non blocking errors on item extraction, plus it should be
    used after ZIP validation. And so no exception should be raised, instead
    all catched item error are logged under logging spacename
    ``cmsplugin_blocks.utils``.

    Arguments:
        instance (object): Saved item container instance to link to item
            objects (to link foreignkey relation).
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
    logger = logging.getLogger("cmsplugin_blocks.utils")

    stored_items = []

    if zip_fileobject:
        for filename in sorted(zip_fileobject.namelist()):
            # Don't process invalid filename or directory
            if filename.endswith("/") or not is_valid_image_filename(filename):
                continue

            # Get archived file from ZIP
            data = zip_fileobject.read(filename)
            if len(data):
                try:
                    # Following code is taken from
                    # django.forms.fields.ImageField: load() could spot a
                    # truncated JPEG, but it loads the entire image in memory,
                    # which is a DoS vector. See #3848 and #18520. verify()
                    # must be called immediately after the constructor.
                    PILimage.open(BytesIO(data)).verify()
                except Exception as e:
                    # if a "bad" file is found we just skip it.
                    msg = "Error verifying image: {}".format(str(e))
                    logger.error(msg)
                    continue

                if hasattr(data, "seek") and isinstance(data.seek,
                                                        collections.Callable):
                    data.seek(0)

                try:
                    item = item_model(**{link_attrname: instance})
                    # Lazy save since we dont have album id yet when creating
                    getattr(
                        item,
                        image_attrname
                    ).save(
                        filename,
                        ContentFile(data),
                        save=False
                    )

                    # Optional string field to fill from filename
                    if label_attrname:
                        setattr(item, label_attrname, filename)
                except Exception as e:
                    msg = "Error creating item from file: {}".format(str(e))
                    logger.error(msg)
                else:
                    # Store created item to be saved further in plugin
                    # 'save_model' method
                    stored_items.append(item)

        # Drop ZIP file object from memory/tempdir when finished
        zip_fileobject.close()

    return stored_items
