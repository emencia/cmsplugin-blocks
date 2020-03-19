# -*- coding: utf-8 -*-
import factory
import io

from PIL import Image as PILimage

from django.core.files import File


def create_image_file(filename=None, format=None):
    """
    Return a File object with a dummy generated image on the fly by PIL.

    Generated image is always a simple blue square.

    Keyword Arguments:
        filename (string): Required filename for generated file, default to
            "blue.jpg". Final filename may be different if all tests use the
            default one, Django will append a hash for uniqueness.
        format (string): Currently not implemented, every generated image is
            JPEG, should allow to generate other formats (PNG, GIF, SVG?).

    Returns:
        django.core.files.File: File object.
    """
    filename = filename or "blue.jpg"

    thumb = PILimage.new("RGB", (100, 100), "blue")
    thumb_io = io.BytesIO()
    thumb.save(thumb_io, format="JPEG")

    return File(thumb_io, name=filename)
