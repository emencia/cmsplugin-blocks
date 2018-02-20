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
                          link_attrname, image_attrname):
    """
    Collect every image from a ZIP as an item object linked to given
    saved instance.

    Once image searching is finished the zip file object is closed.

    Some code has been taken/inspired from 'models.upload.process_zipfile'
    from 'imagestore' app.

    Arguments:
        instance (object): Saved instance to link to item objects.
        zip_fileobject (zipfile.ZipFile): A valid zip file object to search
            for images.
        item_model (model): Model object used to create items objects.
        link_attrname (string): Attribute name used for linking instance to
            item object.
        image_attrname (string): Attribute name used to store image file in
            item object.
    """
    stored_items = []

    if zip_fileobject:
        print("Got a valid ZIP")
        for filename in sorted(zip_fileobject.namelist()):
            # do not process meta files
            if filename.startswith('__'):
                continue

            print(filename)

            # Get archived file from ZIP
            data = zip_fileobject.read(filename)
            if len(data):
                try:
                    # the following is taken from django.forms.fields.ImageField:
                    # load() could spot a truncated JPEG, but it loads the entire
                    # image in memory, which is a DoS vector. See #3848 and #18520.
                    # verify() must be called immediately after the constructor.
                    PILImage.open(BytesIO(data)).verify()
                except Exception as e:
                    # if a "bad" file is found we just skip it.
                    print('Error verifying image: {}'.format(str(e)))
                    continue

                if hasattr(data, 'seek') and isinstance(data.seek, collections.Callable):
                    print('seeked')
                    data.seek(0)

                try:
                    item = item_model(**{link_attrname:instance})
                    getattr(item, image_attrname).save(filename, ContentFile(data))
                    item.save()
                except Exception as e:
                    print('Error creating item from file: {}'.format(str(e)))
                else:
                    stored_items.append(item)

        # Drop ZIP file object from memory/tempdir when finished
        zip_fileobject.close()

    return stored_items
