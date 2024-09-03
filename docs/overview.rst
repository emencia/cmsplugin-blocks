.. _django-smart-media: https://github.com/sveetch/django-smart-media

.. _overview_intro:

========
Overview
========

The goal is to make rich page contents with less involved HTML than directly using
CKeditor. There is a plugin to implement common layout components and each one has its
own fields (title, image, content, link, etc..), they will be used in templates to
the build component parts.


Layout
******

All plugin have a template field so you can easily have multiple layout variants for
each plugins.

Shipped application templates are very basic without any relation to a CSS framework,
you will probably have to edit them all to fit to your layout.


Images
******

All image field are using `django-smart-media`_ library to add some minor features like
upload file preview, soft SVG support and thumbnail (using Sorl thumbnail engine).


Frontend
********

Package only supplies plugin backend parts (DjangoCMS plugin, admin, templates, etc..)
and there is no shipped frontend part like CSS or Javascript for frontend.

The admin and plugin parts are using some internal shipped CSS for forms.

Finally you may see the sandbox templates in the package repository that are using
Bootstrap 5 for demonstration purpose.

Features
********

Basically a feature is CSS class name to add on a plugin.

All plugin have layout features on three different scopes: size, color and extra. The
first is dedicated to CSS class names for size definitions (commonly for grid cells).
The second is for colors (like font color, background color, border color, etc..). And
the third is for everything else that does not fit the first ones.

Also a feature defines the plugins allowed to use the feature. Like a feature that is
not  allowed for the Card plugin won't be available to select in the card features.

.. Warning::
    Currently there is no automatic check about feature usage when you are changing its
    scope or allowed plugins. This means you can remove the Card plugin from allowed
    plugins but the Card plugins that were already using before will still have it.

    However, feature property getter filters out features that are out of scope or
    allowed plugins.

    Until you save again those plugins using filtered out features, their stale feature
    relations will still be stored onto plugins but will be removed once saved again.

    You should take caution about changing scope or remove allowed plugins from
    features.
