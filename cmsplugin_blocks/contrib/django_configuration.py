from ..defaults import (
    BLOCKS_ENABLED_PLUGINS,
    BLOCKS_KNOWED_FEATURES_PLUGINS,
    BLOCKS_FEATURE_PLUGINS,
    BLOCKS_ALBUM_TEMPLATES,
    BLOCKS_CARD_TEMPLATES,
    BLOCKS_CONTAINER_TEMPLATES,
    BLOCKS_HERO_TEMPLATES,
    BLOCKS_SLIDER_TEMPLATES,
    BLOCKS_ALLOWED_IMAGE_EXTENSIONS,
    BLOCKS_MODEL_TRUNCATION_LENGTH,
    BLOCKS_MODEL_TRUNCATION_CHR,
    BLOCKS_MASSUPLOAD_FILESIZE_LIMIT,
)


class CmsBlocksDefaultSettings:
    """
    Default application settings class to use with a "django-configuration" class.

    Example:

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
    """  # noqa: E501

    BLOCKS_ENABLED_PLUGINS = BLOCKS_ENABLED_PLUGINS

    BLOCKS_KNOWED_FEATURES_PLUGINS = BLOCKS_KNOWED_FEATURES_PLUGINS

    BLOCKS_FEATURE_PLUGINS = BLOCKS_FEATURE_PLUGINS

    BLOCKS_ALBUM_TEMPLATES = BLOCKS_ALBUM_TEMPLATES

    BLOCKS_CARD_TEMPLATES = BLOCKS_CARD_TEMPLATES

    BLOCKS_CONTAINER_TEMPLATES = BLOCKS_CONTAINER_TEMPLATES

    BLOCKS_HERO_TEMPLATES = BLOCKS_HERO_TEMPLATES

    BLOCKS_SLIDER_TEMPLATES = BLOCKS_SLIDER_TEMPLATES

    BLOCKS_ALLOWED_IMAGE_EXTENSIONS = BLOCKS_ALLOWED_IMAGE_EXTENSIONS

    BLOCKS_MODEL_TRUNCATION_LENGTH = BLOCKS_MODEL_TRUNCATION_LENGTH

    BLOCKS_MODEL_TRUNCATION_CHR = BLOCKS_MODEL_TRUNCATION_CHR

    BLOCKS_MASSUPLOAD_FILESIZE_LIMIT = BLOCKS_MASSUPLOAD_FILESIZE_LIMIT
