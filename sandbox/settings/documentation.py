"""
Django settings for documentation

This is required since documentation use Sphinx extension 'autodoc' which loads some
application code that import Django and so require a settings file just to setup.
"""
from sandbox.settings.base import *  # noqa: F401,F403
