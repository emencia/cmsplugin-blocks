"""
`django-configuration <https://django-configurations.readthedocs.io/>`_ class that you
can use in your project to load application default settings.

You just have to inherit from it in your settings class: ::

    from configurations import Configuration
    from cmsplugin_blocks.contrib.django_configuration import CmsBlocksDefaultSettings

    class Dev(CmsBlocksDefaultSettings, Configuration):
        DEBUG = True

        BLOCKS_ENABLED_PLUGINS = [
            "CardPlugin",
            "ContainerPlugin",
        ]

This will override only the setting ``BLOCKS_ENABLED_PLUGINS``, all other
application settings will have the default values from
``cmsplugin_blocks.defaults``.
"""
from ..defaults import (
    BLOCKS_ENABLED_PLUGINS,
    BLOCKS_KNOWED_FEATURES_PLUGINS,
    BLOCKS_FEATURE_PLUGINS,
    BLOCKS_ALBUM_TEMPLATES,
    BLOCKS_CARD_TEMPLATES,
    BLOCKS_CONTAINER_TEMPLATES,
    BLOCKS_HERO_TEMPLATES,
    BLOCKS_SLIDER_TEMPLATES,
    BLOCKS_ACCORDION_TEMPLATES,
    BLOCKS_MODEL_TRUNCATION_LENGTH,
    BLOCKS_MODEL_TRUNCATION_CHR,
    BLOCKS_MASSUPLOAD_FILESIZE_LIMIT,
)


class CmsBlocksDefaultSettings:
    """
    Default application settings class to use with a "django-configuration" class.
    """

    BLOCKS_ENABLED_PLUGINS = BLOCKS_ENABLED_PLUGINS

    BLOCKS_KNOWED_FEATURES_PLUGINS = BLOCKS_KNOWED_FEATURES_PLUGINS

    BLOCKS_FEATURE_PLUGINS = BLOCKS_FEATURE_PLUGINS

    BLOCKS_ALBUM_TEMPLATES = BLOCKS_ALBUM_TEMPLATES

    BLOCKS_CARD_TEMPLATES = BLOCKS_CARD_TEMPLATES

    BLOCKS_CONTAINER_TEMPLATES = BLOCKS_CONTAINER_TEMPLATES

    BLOCKS_HERO_TEMPLATES = BLOCKS_HERO_TEMPLATES

    BLOCKS_SLIDER_TEMPLATES = BLOCKS_SLIDER_TEMPLATES

    BLOCKS_ACCORDION_TEMPLATES = BLOCKS_ACCORDION_TEMPLATES

    BLOCKS_MODEL_TRUNCATION_LENGTH = BLOCKS_MODEL_TRUNCATION_LENGTH

    BLOCKS_MODEL_TRUNCATION_CHR = BLOCKS_MODEL_TRUNCATION_CHR

    BLOCKS_MASSUPLOAD_FILESIZE_LIMIT = BLOCKS_MASSUPLOAD_FILESIZE_LIMIT
