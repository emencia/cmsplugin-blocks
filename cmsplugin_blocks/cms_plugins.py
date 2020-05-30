# -*- coding: utf-8 -*-
"""
CMS Plugins installations
"""
from django.conf import settings

from cms.plugin_pool import plugin_pool

from cmsplugin_blocks.plugins.album import AlbumPlugin
from cmsplugin_blocks.plugins.card import CardPlugin
from cmsplugin_blocks.plugins.hero import HeroPlugin
from cmsplugin_blocks.plugins.slider import SliderPlugin


# Register enabled plugins
if "AlbumPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(AlbumPlugin)

if "HeroPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(HeroPlugin)

if "CardPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(CardPlugin)

if "SliderPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(SliderPlugin)
