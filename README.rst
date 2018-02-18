.. _DjangoCMS: https://www.django-cms.org/
.. _djangocms-text-ckeditor: https://github.com/divio/djangocms-text-ckeditor

Emencia DjangoCMS blocks
========================

Some basic component plugins to make content with less involved HTML than directly using CKeditor for everything.

Requires
********

* Python >= 3.4;
* Django>=1.9,<1.12;
* `DjangoCMS`_ >= 3.4,<3.5;
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

And finally apply database migrations.
