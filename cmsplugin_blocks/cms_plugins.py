"""
CMS Plugins installations
"""
from django.conf import settings

from cms.plugin_pool import plugin_pool

from .plugins.album import AlbumPlugin
from .plugins.card import CardPlugin
from .plugins.container import ContainerPlugin
from .plugins.hero import HeroPlugin
from .plugins.slider import SliderPlugin


# Register enabled plugins
if "AlbumPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(AlbumPlugin)

if "HeroPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(HeroPlugin)

if "CardPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(CardPlugin)

if "ContainerPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(ContainerPlugin)

if "SliderPlugin" in settings.BLOCKS_ENABLED_PLUGINS:
    plugin_pool.register_plugin(SliderPlugin)
