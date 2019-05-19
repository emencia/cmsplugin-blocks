=========
Changelog
=========

Version 0.5.2 - 2019/05/18
--------------------------

* Dropped support for Django<1.11;
* Add 'on_delete=models.CASCADE' on Foreign key fields to be compatible with Django>=2.0;
* Fixed changelog;

Version 0.5.1 - 2018/12/19
--------------------------

* Added 'AlbumItem.order' field
* Updated readme;
* Cleaned album template from brief field, close #9;
* Fixed TextEditorWidget which did not use CMS config, close #7;
* Removed django-cms constraint '<3.5';

Version 0.5.0 - 2018/03/09
--------------------------

* Moved zip file validation to ``utils.validate_zip`` method;
* Use sorl thumbnail in default Album template;
* Added basic image file validation from mass upload, close #4;
* Added mass upload file size limit, close #3;
* Added translation catalog for french language;
* Added some CSS in template for Album inline admin form;
* Better README;

Version 0.4.3 - 2018/02/25
--------------------------

* Better plugin form for Album and Card;

Version 0.4.2 - 2018/02/24
--------------------------

* Adjusted 'blank' and 'max_length' field attribute for every models (migrations have been rebooted again);

Version 0.4.1 - 2018/02/24
--------------------------

* Remove long text 'brief' and 'content' field from Album and AlbumItem, replace with a simple 'title' field;
* Added 'order' field to AlbumItem to be able to order ressources list;
* Added mass upload field to AlbumForm;
* Renamed every 'background' fields to 'image' for better naming consistency;

Version 0.4.0 - 2018/02/19
--------------------------

* Added Album plugin;

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
* Added template field to every plugin;

Version 0.2.0 - 2017/10/19
--------------------------

* Added ``establishment_opening`` model/form/plugin/template;
* Cleaned template from private integration to basic HTML;

Version 0.1.2 - 2017/10/18
--------------------------

* Renamed Diptych ``background`` field to ``image``;
* Use Diptych ``alignment`` field value in its template;

Version 0.1.1 - 2017/10/17
--------------------------

* Removed useless basic models and forms from development;

Version 0.1.0 - 2017/10/17
--------------------------

* First commit for banner, slider and diptych blocks;
