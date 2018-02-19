# -*- coding: utf-8 -*-
from django.conf import settings


def get_album_template_choices():
    return settings.BLOCKS_ALBUM_TEMPLATES


def get_album_default_template():
    return settings.BLOCKS_ALBUM_TEMPLATES[0][0]


def get_card_template_choices():
    return settings.BLOCKS_CARD_TEMPLATES


def get_card_default_template():
    return settings.BLOCKS_CARD_TEMPLATES[0][0]


def get_hero_template_choices():
    return settings.BLOCKS_HERO_TEMPLATES


def get_hero_default_template():
    return settings.BLOCKS_HERO_TEMPLATES[0][0]


def get_slider_template_choices():
    return settings.BLOCKS_SLIDER_TEMPLATES


def get_slider_default_template():
    return settings.BLOCKS_SLIDER_TEMPLATES[0][0]
