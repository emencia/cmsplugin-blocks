
=========
Changelog
=========

Version 1.3.2 - Unreleased
--------------------------

* Updated documentation to a new theme;
* Added logo from SVG Repo;
* Restructured and improved documentation;
* Improved Makefile;
* Removed remaining usage of ``os.path`` module in profit of ``pathlib``;
* Removed setting ``BLOCKS_ALLOWED_IMAGE_EXTENSIONS`` in profit of django-smart-media
  setting ``SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS``. You can safely remove the first one
  from your settings;
* Moved documentation Django settings into sandbox;
* Fixed warnings about ``django.core.files.storage.get_storage_class()`` for
  Django>=5.0;
* Update PO catalogs for new translation strings;
* Internal allowed plugin names in Features have been renamed and a data migration is
  in charge to automatically update your data. However this won't work for your
  previously exported dumps, you will need to rename these names your in your dumps
  with the following changes:

  * ``AlbumMain`` becomes ``Album``;
  * ``CardMain`` becomes ``Card``;
  * ``ContainerMain`` becomes ``Container``;
  * ``HeroMain`` becomes ``Hero``;
  * ``SliderMain`` becomes ``Slider``;

  Also remember than since v1.3.1 the names ``AlbumItem`` and ``SliderItem`` are no
  longer valid.

* **Refactored feature getters:**

  * The old method ``get_features()`` has been renamed to a property
    ``flat_features`` with the same behavior (a simple string with ordered
    classnames without any duplicate classname): ::

        >>> foo = Card(...)
        >>> foo.save()
        >>> foo.flat_features
        "bar foo ping"

  * A new property ``scoped_features`` has been introduced, it return a dict indexed
    on scopes: ::

        >>> foo = Card(...)
        >>> foo.save()
        >>> foo.scoped_features
        {
            "size": ["bar", "foo"],
            "color": [],
            "extra": ["foo", "ping"],
        }

  * Getters now enforce scope and plugins filtering so you should never have
    "orphan feature" (like when you change the scope of a feature to ``extra`` but it
    was already used in ``Card.size_features``) returned from getters;


Version 1.3.1 - 2024/09/08
--------------------------

This finalize transition to the new Feature system.

* Implemented new feature system on Album, Container and Slider;
* Album item and Slider item no longer have features;
* Old feature is definitively removed from code and data;


Version 1.3.0 - 2024/07/08
--------------------------

This is an early release for the new Feature system, a new 1.3.x release will come soon
to implement it on every plugin and totally drop the old one.

* Added support for Django 5.0;
* Pinned DjangoCMS to ``<4.0`` since we don't support DjangoCMS 4.X yet;
* Cleaned Tox config from some environment versions to only keep supported bounds (and
  speed up Tox suite);
* Moved history changelog from documentation to root repository;
* Added custom templates in sandbox for better demonstration using Bootstrap components;
* Added a new field ``image_alt`` on every plugin model that have a ``image`` field.
  This is to improve SEO and accessibility. Note than some shipped default template
  like for Hero are not using this new field since they embed image as a background
  without a ``<img/>`` tag;
* **Backward incompatible** Added a new way to manage features:

  * They are splitted into three scopes: size, color and extra;
  * Each scope has its own select input;
  * Features management is centralized in a single model with a scope (size, color and
    extra) and a list of allowed plugins;
  * Allowed plugins for a feature can select it in the proper scope;
  * Plugin model method 'get_features' merge all feature scopes in a single string
    without duplicate classname;

* New features system has currently been implemented for the following plugins:

  * Card;
  * Hero;

* The other plugins are still using the old feature system for now;
* Previous features system will be totally removed and there is no way to migrate
  their data, you will need to create again your features;


Version 1.2.1 - 2023/08/18
--------------------------

A minor version only to update ``.readthedocs.yml`` file to follow service deprecations
changes.


Version 1.2.0 - 2023/07/05
--------------------------

* ``Card.content`` field is no longer required to be filled and empty value is allowed;


Version 1.1.0 - 2023/05/21
--------------------------

* Upgraded to ``django-smart-media>=0.3.0`` to fix plugin form layout on file inputs,
  close #20;
* Cleaned Sass sources from old useless fileinput sources;
* Updated PO and MO files, added missing blank locale for 'en';
* Fixed plugin form to use the proper ``features`` field label;
* Removed all signal receiver ``auto_purge_files_on_change`` usage from all plugins to
  remove a misbehavior with file purge and page publication. This means files related
  to deleted plugin won't be automatically removed anymore, close #22;


Version 1.0.0 - 2023/04/26
--------------------------

Major release to upgrade to modern backend supports and some other improvements.
Your project need to upgrade to the new requirements supports to be able to migrate to
this version and further.

* Removed support for Python less than 3.8;
* Removed support for Django less than 3.2;
* Removed support for DjangoCMS less than 3.11.x;
* Added support for Python from 3.8 to 3.10;
* Added support for Django from 3.2 to 4.1;
* Added support for DjangoCMS from 3.11.x;
* Added new field ``features`` on every block, this field won't be showed on default
  installation since there is no defined features. User have to define them in
  respective plugin settings;
* Added new plugin ``container``;
* Updated default plugin templates, it just inherits from the test one. User will have
  to copy the respective plugin test template to create their own and define them in
  settings;
* Upgrade package setup, Makefile, documentation configuration, Tox configuration;
* Removed included ``SmartMedia`` stuff in profit of ``django-smart-media``
  requirement;
* Rewrited tests;
* Renamed default settings module from ``settings`` to ``defaults``;
* Documentation has been updated for the new plugin ``Container`` and for installation
  document. A next version should comes further to restructurate documentation for
  improvements;
* Added modern sandbox frontend with ``bootstrap=^5.1.3`` built with Node.js;


Version 0.7.1 - 2020/06/06
--------------------------

Release fix for package and documentation publishing on ReadTheDoc.

Manifest file was not accurate and package has been wrongly built
and so was missing the templatetags modules.

The resulting package was incorrect and ReadTheDoc could not build the
documentation.

Version 0.7.0 - 2020/06/06
--------------------------

Better plugin forms ergonomy and documentation.

* Added new setting ``BLOCKS_ENABLED_PLUGINS`` which list plugins to enable
  for usage. Disabled plugins won't be visible but their models are still
  created in your database. **WARNING:** You need to update your project
  settings to add this new setting if you don't include the app settings;
* Added missing field ``title`` for Slide item form;
* Added ``FileInputButton`` widgets to use instead FileInput;
* Added ``ClearableFileInputButton`` widgets to use instead ClearableFileInput;
* Added custom stylesheets for every plugin admin forms to improve their ergonomy;
* Added Boussole to development requirement to build CSS from Sass sources;
* Mute the ``RemovedInDjango40Warning`` warning until DjangoCMS has fixed its
  usage of ``ugettext_lazy``;
* Added missing default settings ``SMART_FORMAT_AVAILABLE_FORMATS``;
* Added documentation in ``docs`` with Sphinx and livereload;

Version 0.6.0 - 2020/05/11
--------------------------

This is a major refactoring which may involve breaking changes for some custom
usages.

* Added full test coverage;
* Added tox configuration;
* Modified every plugin templates to be cleaner and flawless;
* Added ``title`` attribute to SlideItem model;
* Use ``FileField`` instead of ``ImageField`` for image fields in every plugin
  so we can use SVG;
* Add a new template tag ``media_thumb`` with smart format guessing instead of
  Sorl tag ``thumbnail`` on images in every plugin templates;

Version 0.5.2 - 2019/05/18
--------------------------

* Dropped support for Django<1.11;
* Add 'on_delete=models.CASCADE' on Foreign key fields to be compatible with
  Django>=2.0;
* Fixed changelog;

Version 0.5.1 - 2018/12/19
--------------------------

* Added ``AlbumItem.order`` field;
* Updated readme;
* Cleaned album template from brief field, close #9;
* Fixed TextEditorWidget which did not use CMS config, close #7;
* Removed django-cms constraint '<3.5'.

Version 0.5.0 - 2018/03/09
--------------------------

* Moved zip file validation to ``utils.validate_zip`` method;
* Use sorl thumbnail in default Album template;
* Added basic image file validation from mass upload, close #4;
* Added mass upload file size limit, close #3;
* Added translation catalog for french language;
* Added some CSS in template for Album inline admin form;
* Better README.

Version 0.4.3 - 2018/02/25
--------------------------

* Better plugin form for Album and Card.

Version 0.4.2 - 2018/02/24
--------------------------

* Adjusted 'blank' and 'max_length' field attribute for every models
  (migrations have been rebooted again).

Version 0.4.1 - 2018/02/24
--------------------------

* Remove long text 'brief' and 'content' field from Album and AlbumItem,
  replace with a simple 'title' field;
* Added 'order' field to AlbumItem to be able to order ressources list;
* Added mass upload field to AlbumForm;
* Renamed every 'background' fields to 'image' for better naming consistency.

Version 0.4.0 - 2018/02/19
--------------------------

* Added Album plugin.

Version 0.3.0 - 2018/02/19
--------------------------

Reboot:

* Better Makefile;
* Added dev requirements;
* Updated 'setup.py' requirements;
* Removed establishment opening plugin (too much specific for now);
* Reset initial migrations (totally backward incompatible);
* Moved Banner to Hero;
* Moved Diptych to Card;
* Added template field to every plugin.

Version 0.2.0 - 2017/10/19
--------------------------

* Added ``establishment_opening`` model/form/plugin/template;
* Cleaned template from private integration to basic HTML.

Version 0.1.2 - 2017/10/18
--------------------------

* Renamed Diptych ``background`` field to ``image``;
* Use Diptych ``alignment`` field value in its template.

Version 0.1.1 - 2017/10/17
--------------------------

* Removed useless basic models and forms from development.

Version 0.1.0 - 2017/10/17
--------------------------

* First commit for banner, slider and diptych blocks.
