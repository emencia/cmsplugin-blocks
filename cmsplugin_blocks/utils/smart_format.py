# -*- coding: utf-8 -*-
from django.conf import settings


AVAILABLE_FORMATS = getattr(settings, "SMART_FORMAT_AVAILABLE_FORMATS", [
    ("jpg", "JPEG"),
    ("jpeg", "JPEG"),
    ("png", "PNG"),
    ("gif", "GIF"),
    ("svg", "SVG"),
])


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

            for fileext, formatname in AVAILABLE_FORMATS:
                if ext == fileext:
                    return formatname

        return None
