.. _DjangoCMS: https://www.django-cms.org/
.. _sorl-thumbnail: https://github.com/mariocesar/sorl-thumbnail
.. _djangocms-text-ckeditor: https://github.com/divio/djangocms-text-ckeditor

Emencia DjangoCMS blocks
========================

A set of DjangoCMS plugins to make content with less involved HTML than
directly using CKeditor for everything.

This just supply some plugins with a default basic template. There is no CSS,
Javascript or anything else like frontend integration.

Requires
********

* Python >= 3.4;
* Django>=1.9,<1.12;
* Pillow;
* `sorl-thumbnail`_;
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
        'sorl.thumbnail',
        'cmsplugin_blocks',
    )

Then load its settings from your settings file: ::

    from cmsplugin_blocks import *

And finally apply database migrations.

Available components
********************

Album

    Available fields:

    * title;
    * template;

    Album have related items *AlbumItem* which are added/edited through inline form.

    Available *AlbumItem* items fields:

    * image;
    * content;

Card

    Available fields:

    * alignment;
    * template;
    * image;
    * content;

Hero

    Available fields:

    * template;
    * image;
    * content;

Slider

    Available fields:

    * title;
    * template;

    Available *SlideItem* items fields:

    * image;
    * content;
    * order;
    * link_name;
    * link_url;
    * link_open_blank;

    Slider have related items *SlideItem* which are added/edited through
    inline form.

Mass upload
***********

There is a field "mass upload" on Album that attemp a valid ZIP archive file
to create new album items. Each image file from ZIP archive will be added as
a new album item using image filename as item title. Scanning ZIP archive for
image files is recursive and so the full image filename is used, even its
relative path inside archive.

Settings
********

These are default settings you may override in your own project settings.

BLOCKS_ALBUM_TEMPLATES
    Available templates to render an Album object and its items. Default
    setting value contains only one default template.
BLOCKS_CARD_TEMPLATES
    Available templates to render an Card object. Default
    setting value contains only one default template.
BLOCKS_HERO_TEMPLATES
    Available templates to render an Hero object. Default
    setting value contains only one default template.
BLOCKS_SLIDER_TEMPLATES
    Available templates to render an Slider object and its items. Default
    setting value contains only one default template.
BLOCKS_TEMP_DIR
    Path to directory where to store temporary ZIP archive for mass upload.
    Default to `temp/`.
BLOCKS_MASSUPLOAD_IMAGE_TYPES
    Allowed images file extensions in ZIP archive for mass upload. Default
    value allow `jpg`, `jpeg`, `svg`, `gif` and `png`.
BLOCKS_MASSUPLOAD_FILESIZE_LIMIT
    Maximum file size (in bytes) allowed for ZIP archive for mass upload.
    Default to `429916160` (50MiO).

A note about djangocms-text-ckeditor
************************************

djangocms-text-ckeditor get configurations from
``CKEDITOR_SETTINGS["toolbar_HTMLField"]`` when used from plugin, you may have
to duplicate it from ``CKEDITOR_SETTINGS["toolbar_CMS"]`` if you want to share
the same configuration for CKeditor from CMS pages and CKeditor from blocks
plugins.
