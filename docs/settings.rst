.. _settings_intro:

========
Settings
========

These are the default settings you can override in your project settings.

.. automodule:: cmsplugin_blocks.defaults
   :members:

.. Note::

    Instead, if your project use
    `django-configuration <https://django-configurations.readthedocs.io/en/stable/>`_,
    your settings class can inherits from
    ``from cmsplugin_blocks.contrib.django_configuration import CmsBlocksDefaultSettings``
    and the settings class from SmartMedia see
    `SmartMedia configuration documentation <https://django-smart-media.readthedocs.io/en/latest/install.html#configuration>`_.

About CKEditor settings
***********************

``djangocms-text-ckeditor`` get configurations from
``CKEDITOR_SETTINGS["toolbar_HTMLField"]`` when used from external plugin but
use ``CKEDITOR_SETTINGS["toolbar_CMS"]`` for internal plugin like its basic
TextPlugin.

You will have to copy ``toolbar_CMS`` config to ``toolbar_HTMLField`` if
you want to share the same configuration for every plugins: ::

    CKEDITOR_SETTINGS["toolbar_HTMLField"] = CKEDITOR_SETTINGS["toolbar_CMS"]
