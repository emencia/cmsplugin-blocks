# -*- coding: utf-8 -*-
from django import template

from sorl.thumbnail.shortcuts import get_thumbnail

from cmsplugin_blocks.exceptions import (
    InvalidFormatError, IncompatibleSvgToBitmap, IncompatibleBitmapToSvg
)
from cmsplugin_blocks.utils import (
    AVAILABLE_FORMAT_EXTENSIONS, SmartFormatMixin
)

register = template.Library()


@register.simple_tag
def media_format_url(source, geometry, *args, **kwargs):
    """
    Determine the right format and return the Sorl thumb file url path for
    given image file.

    Arguments:
        source (object): Either a FileField or an ImageField.
        geometry (string): Geometry string as expected by Sorl. It should be
            something like ``200`` for 200px width and automatic height or
            ``200x100`` for 200px width and 100px height.
        *args: Not used, there is no other expected positionnal arguments.
        **kwargs: Keyword arguments are passed to Sorl, watch its documentation
            for more details.

    Keyword Arguments:
        format (string): Either ``PNG``, ``JPEG``, ``GIF``, ``SVG`` or ``auto``.

            * ``PNG``, ``JPEG`` and ``GIF`` enforce the thumb format no matter
              the source image format. Be careful to not enforce a format where
              a SVG is a possible source format, since Sorl can't read SVG.
            * ``SVG`` will not produce any thumb, just return the same path
              than the source one since SVG does not need a thumb.
            * ``auto`` format automatically find and use the same format than
              the source image. This is the recommended way.

            When argument is empty the default value is ``auto``.

    Return:
        sorl.thumbnail.images.ImageFile: Sorl ImageFile instance for created
        thumb.
    """
    # Safe return when there is no source file
    # NOTE: Should trigger a warning log ?
    if not source:
        return None

    required_format = kwargs.pop("format", "auto")
    source_extension = source.name.split(".")[-1].lower()

    # Vector format does not create a thumb and so just return original
    # source url

    # Automatic format guess
    if required_format.lower() == "auto":
        required_format = SmartFormatMixin().media_format(source)
    # Specific SVG format
    elif required_format.lower() == "svg":
        # A bitmap file cannot be converted to a SVG
        if source_extension != "svg":
            msg = ("Incompatible required format (SVG) with source format "
                   "(Bitmap).")
            raise IncompatibleBitmapToSvg(msg.format(
                format_name=required_format.lower(),
            ))
        # SVG to SVG is correct (nothing to do)
        return source
    # Unknown format
    elif required_format.lower() not in AVAILABLE_FORMAT_EXTENSIONS:
        msg = ("Required format '{format_name}' does not match available "
               "formats: {available}")
        raise InvalidFormatError(msg.format(
            format_name=required_format.lower(),
            available=", ".join(AVAILABLE_FORMAT_EXTENSIONS),
        ))
    # SVG source with required bitmap format
    elif source_extension == "svg":
        msg = ("Incompatible required format (Bitmap) with source format "
               "(SVG).")
        raise IncompatibleSvgToBitmap(msg.format(
            format_name=required_format.lower(),
        ))

    kwargs["format"] = required_format

    # For SVG source, just returns the source file
    if required_format == "SVG":
        return source

    # Here we assume the format is ok, if it has been manually defined, user
    # is responsible about possible error with its content
    return get_thumbnail(source, geometry, **kwargs)
