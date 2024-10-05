from django.utils.translation import gettext_lazy as _


BLOCKS_ENABLED_PLUGINS = [
    "AccordionPlugin",
    "AlbumPlugin",
    "CardPlugin",
    "ContainerPlugin",
    "HeroPlugin",
    "SliderPlugin",
]
"""
Enabled plugins to register. Unregistered plugin models are still created but
not available anymore in DjangoCMS. This should be safe to edit to enable or disable
plugins even with existing data, however existing plugin in pages will still be present.
"""

BLOCKS_KNOWED_FEATURES_PLUGINS = [
    "Accordion",
    "Album",
    "Card",
    "Container",
    "Hero",
    "Slider",
]
"""
List of knowed plugin names where to enable features.

Developers should be aware when naming keys since we use a basic ``contains``
lookup expression on comma separated string, key names must be unique and can not be
matched with a part of another key. Like ``Slider`` could match ``Slider`` or
``SliderItem``, so in this case we would prefer to use names likes ``Slider`` and
``SlideItem``.

.. Warning::
    You should not change this setting since they are used internally. Developers
    that would want to implement features on their own plugins may add them here but
    carefully.

    If you just want to disable some available cmsplugin-blocks plugins from features,
    see ``BLOCKS_FEATURE_PLUGINS``.
"""

BLOCKS_FEATURE_PLUGINS = [
    ("Accordion", _("Accordion")),
    ("Album", _("Album")),
    ("Card", _("Card")),
    ("Container", _("Container")),
    ("Hero", _("Hero")),
    ("Slider", _("Slider")),
]
"""
Available plugins to allow on Features.
"""

BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES = False
"""
Options for Feature field ``value`` to allows to input multiple CSS classnames divided
by a whitespace like: ::

    col col-md-6 col-lg-4

On default, it is false and you are only allowed to a input single CSS class name on
each Feature field ``value``.

Be aware that you won't be able to import a JSON dump of features from a project which
does not use the same value of this setting.
"""

BLOCKS_ACCORDION_TEMPLATES = [
    ("cmsplugin_blocks/accordion/default.html", "Default"),
]
"""
Available template choices to render a Accordion object and its items.
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
Maximum file size (in bytes) allowed for ZIP archive from mass upload feature.

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
