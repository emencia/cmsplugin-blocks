.. _DjangoCMS: https://www.django-cms.org/
.. _djangocms-text-ckeditor: https://github.com/divio/djangocms-text-ckeditor

Emencia DjangoCMS blocks
========================

A serie of `DjangoCMS`_ plugin to collect common content blocks to use in CMS pages.

**This is Alpha stage, it may break in future, things can disappear, etc..**. You are advised.

Requires
********

* Python >= 3.4;
* `DjangoCMS`_ >= 3.3;
* `djangocms-text-ckeditor`_;

Install
*******

First install package ::

    pip install cmsplugin-blocks

Add it to your installed Django apps in settings like this : ::

    INSTALLED_APPS = (
        ...
        'cms',
        'djangocms_text_ckeditor',
        'cmsplugin_blocks',
    )

Then load its settings from your settings file: ::

    from cmsplugin_blocks import *

And finally apply its migrations.
