"""
These are wrappers for field defaults and choices values to be used as a callable.

You should always use these callables to get defaults or choices values instead of
directly use their related settings.

Callables for defaults return a single string. Callables for choices
return a tuple of choice tuples. None of them accept any argument.
"""
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def get_accordion_template_choices(): return settings.BLOCKS_ACCORDION_TEMPLATES


def get_accordion_template_default(): return settings.BLOCKS_ACCORDION_TEMPLATES[0][0]


def get_album_template_choices(): return settings.BLOCKS_ALBUM_TEMPLATES


def get_album_template_default(): return settings.BLOCKS_ALBUM_TEMPLATES[0][0]


def get_card_template_choices(): return settings.BLOCKS_CARD_TEMPLATES


def get_card_template_default(): return settings.BLOCKS_CARD_TEMPLATES[0][0]


def get_container_template_choices(): return settings.BLOCKS_CONTAINER_TEMPLATES


def get_container_template_default(): return settings.BLOCKS_CONTAINER_TEMPLATES[0][0]


def get_hero_template_choices(): return settings.BLOCKS_HERO_TEMPLATES


def get_hero_template_default(): return settings.BLOCKS_HERO_TEMPLATES[0][0]


def get_slider_template_choices(): return settings.BLOCKS_SLIDER_TEMPLATES


def get_slider_template_default(): return settings.BLOCKS_SLIDER_TEMPLATES[0][0]


def get_feature_plugin_choices(): return settings.BLOCKS_FEATURE_PLUGINS


def get_feature_plugin_default(): return settings.BLOCKS_FEATURE_PLUGINS[0][0]


def get_value_help_text():
    """
    Get feature value field help text that change depending setting
    ``BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES``.

    Returns:
        string: The help text to display in form for ``Feature.value``.
    """
    if settings.BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES is True:
        return _("A list of valid CSS classnames divided with a whitespace.")
    else:
        return _("A valid CSS classname.")
