# -*- coding: utf-8 -*-
"""
CMS Plugins installations
"""
from cms.plugin_pool import plugin_pool

from cmsplugin_blocks.plugins.album import AlbumPlugin
from cmsplugin_blocks.plugins.card import CardPlugin
from cmsplugin_blocks.plugins.hero import HeroPlugin
from cmsplugin_blocks.plugins.slider import SliderPlugin


# TODO: May depend from a setting to only load some plugin
plugin_pool.register_plugin(AlbumPlugin)
plugin_pool.register_plugin(HeroPlugin)
plugin_pool.register_plugin(CardPlugin)
plugin_pool.register_plugin(SliderPlugin)
