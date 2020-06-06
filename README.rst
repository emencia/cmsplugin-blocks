.. _DjangoCMS: https://www.django-cms.org/
.. _sorl-thumbnail: https://github.com/mariocesar/sorl-thumbnail
.. _djangocms-text-ckeditor: https://github.com/divio/djangocms-text-ckeditor

Emencia DjangoCMS blocks
========================

A set of DjangoCMS plugins for content structures.

Goal is to make content with less involved HTML than directly using CKeditor
for everything and involve to edit content HTML source to create advanced
structures.

This just supply some plugins with a default basic template. There is no CSS,
Javascript or anything else like frontend integration.

Also there is some improvements on thumbnails with smart format detection and
better Django file upload field ergonomy.

Links
*****

* Read the documentation on `Read the docs <https://cmspluginblocks.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/cmsplugin-blocks>`_;
* Clone it on its `Github repository <https://github.com/emencia/cmsplugin-blocks>`_;

Dependancies
************

* Python>=3.5;
* Django>=2.0;
* Pillow;
* `sorl-thumbnail`_;
* `DjangoCMS`_ >= 3.6;
* `djangocms-text-ckeditor`_;

Support
*******

Application is tested against the following versions:

* Python 3.4 to 3.6;
* Django 2.0 to 3.0;
* DjangoCMS 3.6 to 3.7;
