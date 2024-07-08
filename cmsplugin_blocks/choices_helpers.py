"""
These are wrapper for field default and choice values to be used as callable.

You should always these callable to get default or choices values instead of directly
use their related settings.

Callables for default return a single item, commonly a string. Callables for choices
return a tuple of choice tuples. None of them accept any argument.
"""
from django.conf import settings


def get_album_feature_choices():
    return settings.BLOCKS_ALBUM_FEATURES


def get_albumitem_feature_choices():
    return settings.BLOCKS_ALBUMITEM_FEATURES


def get_album_template_choices():
    return settings.BLOCKS_ALBUM_TEMPLATES


def get_album_template_default():
    return settings.BLOCKS_ALBUM_TEMPLATES[0][0]


def get_card_template_choices():
    return settings.BLOCKS_CARD_TEMPLATES


def get_card_template_default():
    return settings.BLOCKS_CARD_TEMPLATES[0][0]


def get_container_feature_choices():
    return settings.BLOCKS_CONTAINER_FEATURES


def get_container_template_choices():
    return settings.BLOCKS_CONTAINER_TEMPLATES


def get_container_template_default():
    return settings.BLOCKS_CONTAINER_TEMPLATES[0][0]


def get_hero_template_choices():
    return settings.BLOCKS_HERO_TEMPLATES


def get_hero_template_default():
    return settings.BLOCKS_HERO_TEMPLATES[0][0]


def get_slider_feature_choices():
    return settings.BLOCKS_SLIDER_FEATURES


def get_slideritem_feature_choices():
    return settings.BLOCKS_SLIDERITEM_FEATURES


def get_slider_template_choices():
    return settings.BLOCKS_SLIDER_TEMPLATES


def get_slider_template_default():
    return settings.BLOCKS_SLIDER_TEMPLATES[0][0]


def get_feature_plugin_choices():
    return settings.BLOCKS_FEATURE_PLUGINS


def get_feature_plugin_default():
    return settings.BLOCKS_FEATURE_PLUGINS[0][0]
