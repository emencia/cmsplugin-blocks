
======================
Thumbnail smart format
======================

It is an additional layer around Sorl thumbnail usage. Sorl is a wonderful
library but default behavior is to create every thumbnail on the same format,
commonly JPEG.

This is the included way default plugin templates, if you make custom templates
it is recommended to use it, however this is at your responsibility.


Benefits
********

* A better respect to image quality because converting a PNG to a JPEG thumbnail
  may cause deterioration.
* A safe way to include SVG images without too many hacks. Since Sorl can not
  manage SVG, smart-format will pass thumbnail creation on this format and just
  use the original image;
* Avoid possible errors with RGB(A) mode, a GIF create a GIF thumbnail;

.. Note::

    It stands on a naive technique which trust the image file extension to be
    correctly accorded to its format such as a "foo.jpg" file is a JPEG image.


How it is implemented
*********************

There is two sides:

* A template tag ``media_thumb`` to create a thumbnail using Sorl with given
  paramaters. It is used on every image field in plugin templates;
* Every plugin model have a ``get_image_format`` method which returns the
  image format, when template tag is in format mode ``auto`` (the default) it
  will seek for this method to automatically resolve the format to use to
  create image thumbnail;

Obviously, you can choose to enforce a special format over the original image
format from your template tag usage.


Template tag usage
******************

.. autofunction:: cmsplugin_blocks.templatetags.smart_format.media_thumb
