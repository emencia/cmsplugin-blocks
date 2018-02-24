# -*- coding: utf-8 -*-
import collections
from io import BytesIO

# This is probably for Python 2/3 support although we dont support Py2
try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _


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
            # do not process meta files
            if filename.startswith('__'):
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
