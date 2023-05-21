.. _DjangoCMS: https://www.django-cms.org/
.. _sorl-thumbnail: https://github.com/mariocesar/sorl-thumbnail
.. _djangocms-text-ckeditor: https://github.com/divio/djangocms-text-ckeditor
.. _django-smart-media: https://github.com/sveetch/django-smart-media
.. _django-configuration: https://django-configurations.readthedocs.io/en/stable/


Emencia DjangoCMS blocks
========================

A set of DjangoCMS plugins for structured contents in CMS pages.

The goal is to make rich page contents with less involved HTML than directly using
CKeditor. There is a plugin to implement common layout components and each one has its
own fields (title, image, content, link, etc..), they will be used in templates to
the build component parts.

All plugin have a template field and possible CSS feature classes to select, so you can
make multiple component layout variants. You will define these available templates and
CSS feature classes from your settings.

Plugins only supply plugin backend parts, there is no shipped frontend part like CSS or
Javascript in this package.


Features
********

* Many plugins to implement some common layout components;

  * Album;
  * Card;
  * Container;
  * Hero;
  * Slider;

* Album can be filled from a ZIP with images;
* Included image thumbnailing;
* SVG soft support in image fields;
* Full test coverage;
* Included class for default settings with `django-configuration`_ (this is optional);


Dependancies
************

* Python>=3.8;
* Django>=3.2;
* `DjangoCMS`_>=3.11.0;
* `djangocms-text-ckeditor`_>=5.0.1;
* `django-smart-media`_>=0.3.0;


Links
*****

* Read the documentation on `Read the docs <https://cmspluginblocks.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/cmsplugin-blocks>`_;
* Clone it on its `Github repository <https://github.com/emencia/cmsplugin-blocks>`_;
