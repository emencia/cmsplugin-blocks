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

Then import the default :ref:`settings_intro`: ::

    from smart_media.settings import *
    from cmsplugin_blocks.defaults import *

You may not import these defaults but you will have to define them all in your project
settings.

Finally you will have to apply database migrations.
