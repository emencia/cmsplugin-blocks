BLOCKS_ENABLED_PLUGINS = [
    "AlbumPlugin",
    "CardPlugin",
    "HeroPlugin",
    "SliderPlugin",
]
"""
Enabled plugins to register. Unregistered plugin models are still created but
not available anymore in DjangoCMS.
"""

BLOCKS_ALBUM_TEMPLATES = [
    ('cmsplugin_blocks/album/default.html', 'Default'),
]
"""
Available template choices to render an Album object and its items.
"""

BLOCKS_CARD_TEMPLATES = [
    ('cmsplugin_blocks/card/default.html', 'Default'),
]
"""
Available template choices to render an Card object.
"""

BLOCKS_HERO_TEMPLATES = [
    ('cmsplugin_blocks/hero/default.html', 'Default'),
]
"""
Available template choices to render an Hero object.
"""

BLOCKS_SLIDER_TEMPLATES = [
    ('cmsplugin_blocks/slider/default.html', 'Default'),
]
"""
Available template choices to render a Slider object and its items.
"""

BLOCKS_ALLOWED_IMAGE_EXTENSIONS = [
    "jpg",
    "jpeg",
    "svg",
    "gif",
    "png",
]
"""
Allowed image file extensions for images. This is used in plugin form with
image field for validation and also for allowed formats in ``media_thumb``
template tag (smart format).

Note that image field validation is naively based on file extension, not on
the real image format so this could be tricked.

You should accord this list with setting ``SMART_FORMAT_AVAILABLE_FORMATS``.
"""

BLOCKS_MODEL_TRUNCATION_LENGTH = 4
"""
Word length limit for model string representation truncation.

This is used in every model string which are displayed in their plugin resume
in DjangoCMS placeholder menu.

With a length of 4 words, an object title "Foo bar Lorem ipsum ping" will be
cutted to "Foo bar Lorem ipsum".
"""

BLOCKS_MODEL_TRUNCATION_CHR = "..."
"""
Truncation string added to the end of an object title when it have been
truncated when over the word limit.

Use an empty string if you don't want any character at the end of truncation.
"""

BLOCKS_MASSUPLOAD_FILESIZE_LIMIT = 42991616
"""
Maximum file size allowed for mass upload feature.
Maximum file size (in bytes) allowed for ZIP archive for mass upload.

This is a limit at Django level so files are still stored until post validation.

You should mind to configure a limit on your webserver to avoid basic attacks
with very big files.

Value could be something like:

* ``5242880`` for ~5MiO;
* ``10485760`` for ~10MiO;
* ``42991616`` for ~50MiO.

See:

https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
"""

SMART_FORMAT_AVAILABLE_FORMATS = [
    ("jpg", "JPEG"),
    ("jpeg", "JPEG"),
    ("png", "PNG"),
    ("gif", "GIF"),
    ("svg", "SVG"),
]
"""
Available formats for template tag ``media_thumb``.

This is a list of tuples such as ``(extension, name)``, where ``extension`` is
a lowercase file extension and ``name`` is the format name as expected from
Sorl (excepted for SVG which is a very special format).

You should accord this list with setting ``BLOCKS_ALLOWED_IMAGE_EXTENSIONS``.
"""
