.. _djangocms-text: https://github.com/django-cms/djangocms-text
.. _djangocms-text-ckeditor: https://github.com/django-cms/djangocms-text-ckeditor
.. _Tiptap: https://tiptap.dev/
.. _CKEditor v4: https://ckeditor.com/ckeditor-4/
.. _CKEditor v5: https://ckeditor.com/ckeditor-5/
.. _Quill: https://quilljs.com/
.. _TinyMCE: https://www.tiny.cloud/

.. _editors_intro:

============
Rich editors
============

Some of plugins contain a field to write rich text (with formatting) if a rich text
editor package is installed, we currently support the following ones.

If none of them are installed DjangoCMS blocks will fallback to the builtin
`Django Textarea widget <https://docs.djangoproject.com/en/5.1/ref/forms/widgets/#textarea>`_.

.. Note::
    You will need to install the editor package on your own then mount it in
    setting ``INSTALLED_APPS`` before DjangoCMS blocks.


djangocms-text-ckeditor
***********************

`djangocms-text-ckeditor`_ was the legacy editor package before DjangoCMS v4 era.

It is on the way to be deprecated mostly because CKEditor v4 is abandonned, known
to include some security issues and it can be migrated to v5 because of incompatible
licensing.

.. Attention::
    We are planning to drop support of this package in a next major release.


djangocms-text
**************

`djangocms-text`_ is the modern choice editor package since DjangoCMS v4 era.

Opposed to legacy editor it is not tied to CKEditor anymore and allow to use another
supported editor which are:

* `Tiptap`_ (default);
* `CKEditor v4`_;
* `CKEditor v5`_;
* `Quill`_ (some CMS text plugin features are not available);
* `TinyMCE`_ (some CMS text plugin features are not available);

If you just want to migrate an existing project you should choose to enable the
*CKEditor v4* which should work as the legacy editor.


About CKEditor settings
***********************

``djangocms-text-ckeditor`` get configurations from
``CKEDITOR_SETTINGS["toolbar_HTMLField"]`` when used from external plugin but
use ``CKEDITOR_SETTINGS["toolbar_CMS"]`` for internal plugin like its basic
TextPlugin.

You will have to copy ``toolbar_CMS`` config to ``toolbar_HTMLField`` if
you want to share the same configuration for every plugins: ::

    CKEDITOR_SETTINGS["toolbar_HTMLField"] = CKEDITOR_SETTINGS["toolbar_CMS"]
