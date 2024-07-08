"""

.. HINT::

    All feature choices are list of tuple. First choice item is a valid CSS class name
    (not a selector, only alphanumeric, ``-`` and ``_``), second item is the label for
    select option. As an exemple: ::

        BLOCKS_ALBUM_FEATURES = [
            ("foo", "Foo"),
            ("text-center", "Centered text"),
        ]

"""
from django.utils.translation import gettext_lazy as _


BLOCKS_ENABLED_PLUGINS = [
    "AlbumPlugin",
    "CardPlugin",
    "ContainerPlugin",
    "HeroPlugin",
    "SliderPlugin",
]
"""
Enabled plugins to register. Unregistered plugin models are still created but
not available anymore in DjangoCMS.
"""

BLOCKS_ALBUM_FEATURES = []
"""
Available feature classes for Album model.
"""

BLOCKS_ALBUMITEM_FEATURES = []
"""
Available feature classes for AlbumItem model.
"""

BLOCKS_CONTAINER_FEATURES = []
"""
Available feature classes for Container model.
"""

BLOCKS_SLIDER_FEATURES = []
"""
Available feature classes for Slider model.
"""

BLOCKS_SLIDERITEM_FEATURES = []
"""
Available feature classes for SliderItem model.
"""

BLOCKS_KNOWED_FEATURES_PLUGINS = [
    "AlbumMain",
    "AlbumItem",
    "CardMain",
    "HeroMain",
    "ContainerMain",
    "SliderMain",
    "SliderItem",
]
"""
List of knowed plugin names where to enable features.

.. Warning::
    You should not change this setting since they are used internally. Developpers
    that would want to implement features on their own plugins may add them here but
    carefully.

    If you just want to removed some allowed cmsplugin-blocks plugins from features,
    see ``BLOCKS_FEATURE_PLUGINS``.
"""

BLOCKS_FEATURE_PLUGINS = [
    ("AlbumMain", _("Album")),
    ("AlbumItem", _("Album item")),
    ("CardMain", _("Card")),
    ("HeroMain", _("Hero")),
    ("ContainerMain", _("Container")),
    ("SliderMain", _("Slider")),
    ("SliderItem", _("Slider item")),
]
"""
Available plugins to allow on Features.

Developers should be aware when naming keys here, since we use a basic ``contains``
lookup expression on comma separated string, key names must be unique and can not be
matched with a part of another key. Like ``Slider`` could match ``SliderMain`` or
``SliderItem``.
"""

BLOCKS_ALBUM_TEMPLATES = [
    ("cmsplugin_blocks/album/default.html", "Default"),
]
"""
Available template choices to render an Album object and its items.
"""

BLOCKS_CARD_TEMPLATES = [
    ("cmsplugin_blocks/card/default.html", "Default"),
]
"""
Available template choices to render an Card object.
"""

BLOCKS_CONTAINER_TEMPLATES = [
    ("cmsplugin_blocks/container/default.html", "Default"),
]
"""
Available template choices to render an Container object.
"""

BLOCKS_HERO_TEMPLATES = [
    ("cmsplugin_blocks/hero/default.html", "Default"),
]
"""
Available template choices to render an Hero object.
"""

BLOCKS_SLIDER_TEMPLATES = [
    ("cmsplugin_blocks/slider/default.html", "Default"),
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
