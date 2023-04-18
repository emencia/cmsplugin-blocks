"""
Specific application exceptions.
"""


class SmartFormatBaseException(Exception):
    """
    Base for every SmartFormat template tag exceptions.
    """
    pass


class InvalidFormatError(SmartFormatBaseException):
    """
    Exception to be raised from smart_format template tag when given format is
    not invalid.
    """
    pass


class IncompatibleSvgToBitmap(SmartFormatBaseException):
    """
    Exception to be raised from smart_format template tag when required format
    is a Bitmap formt but the source is a SVG.
    """
    pass


class IncompatibleBitmapToSvg(SmartFormatBaseException):
    """
    Exception to be raised from smart_format template tag when required format
    is a SVG but the source is a Bitmap.
    """
    pass
