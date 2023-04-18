.. _intro_install:

=======
Install
=======

Install package in your environment : ::

    pip install cmsplugin-blocks

For development install see :ref:`install_development`, this is also a good way to
quick start a demonstration since development install have a demonstration site ready
to run.

Configuration
*************

.. HINT::
    Your project will need to be correctly configured for
    `DjangoCMS <https://docs.django-cms.org/en/latest/>`_, this document won't treat
    about it.

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "sorl.thumbnail",
        "smart_media",
        "cmsplugin_blocks",
    )


.. NOTE::
    * ``cmsplugin_blocks`` need to be added after DjangoCMS;
    * If your project use ``easy_thumbnails``, you will have to put Sorl and SmartMedia
      before it, see `SmartMedia configuration documentation <https://django-smart-media.readthedocs.io/en/latest/install.html#configuration>`_.

Then import the default settings: ::

    from smart_media.settings import *
    from cmsplugin_blocks.defaults import *

You may not import these defaults but you will have to define them all in your project
settings.

.. Note::

    Instead, if your project use
    `django-configuration <https://django-configurations.readthedocs.io/en/stable/>`_,
    your settings class can inherits from
    ``from cmsplugin_blocks.contrib.django_configuration import CmsBlocksDefaultSettings``
    and the settings class from SmartMedia see
    `SmartMedia configuration documentation <https://django-smart-media.readthedocs.io/en/latest/install.html#configuration>`_.

Finally you will have to apply database migrations.


Settings
********

These are the default settings you can override in your project settings.

.. automodule:: cmsplugin_blocks.defaults
   :members:

About CKEditor settings
***********************

``djangocms-text-ckeditor`` get configurations from
``CKEDITOR_SETTINGS["toolbar_HTMLField"]`` when used from external plugin but
use ``CKEDITOR_SETTINGS["toolbar_CMS"]`` for internal plugin like its basic
TextPlugin.

You will have to copy ``toolbar_CMS`` config to ``toolbar_HTMLField`` if
you want to share the same configuration for every plugins: ::

    CKEDITOR_SETTINGS["toolbar_HTMLField"] = CKEDITOR_SETTINGS["toolbar_CMS"]
