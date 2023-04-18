
=========
Changelog
=========

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
