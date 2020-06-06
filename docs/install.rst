.. _intro_install:

=======
Install
=======

Install package in your environment : ::

    pip install cmsplugin-blocks

Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        'cms',
        'djangocms_text_ckeditor',
        'sorl.thumbnail',
        'cmsplugin_blocks',
    )

``cmsplugin_blocks`` should be added after DjangoCMS stuff and Sorl.

Then load its settings from your settings file: ::

    from cmsplugin_blocks.settings import *

And finally apply database migrations.

Settings
********

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

.. automodule:: cmsplugin_blocks.settings
   :members:

A note about CKEditor configuration
***********************************

``djangocms-text-ckeditor`` get configurations from
``CKEDITOR_SETTINGS["toolbar_HTMLField"]`` when used from external plugin but
use ``CKEDITOR_SETTINGS["toolbar_CMS"]`` for internal plugin like its basic
TextPlugin.

You will have to copy ``toolbar_CMS`` config to ``toolbar_HTMLField`` if
you want to share the same configuration for every plugins: ::

    CKEDITOR_SETTINGS["toolbar_HTMLField"] = CKEDITOR_SETTINGS["toolbar_CMS"]

