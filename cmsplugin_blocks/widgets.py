# -*- coding: utf-8 -*-
from django.forms.widgets import FileInput, ClearableFileInput


class FileInputButtonBase(FileInput):
    """
    A simple FileInput override to use a custom template.

    The base version does not include the required medias so you can include
    them yourself in your form controler, this is a good idea in some
    environment like DjangoCMS which needs to use a lot of "!important" marks
    to override the admin stylesheets, which are not part of this widget
    stylesheets.

    Default behavior if not "class" attribute is given is to apply the CSS
    classname "fileinputbutton__input" to the input.

    .. Note::
        When your input file enable the "multiple" attribute to accept more
        than one file, label input will be rendered to a default string like
        "4 files" which is not translatable (this is done in the Javascript
        source).

        If you want a translatable string just pass it to widget instance
        attribute ``data-multiple-caption`` like: ::

            FileInputButton(attrs={
                "data-multiple-caption": gettext_lazy("{count} files selected")
            })

        Pattern ``{count}`` will be replaced with the number of selected files.
    """
    template_name = "cmsplugin_blocks/fileinputbutton/file.html"

    def __init__(self, attrs=None):
        default_attrs = {'class': 'fileinputbutton__input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class ClearableFileInputButtonBase(ClearableFileInput):
    """
    Alike "FileInputButtonBase" but to extend the clearable file input.

    This won't support the "multiple" input file feature.
    """
    template_name = "cmsplugin_blocks/fileinputbutton/clearable_file_input.html"

    def __init__(self, attrs=None):
        default_attrs = {'class': 'fileinputbutton__input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class FileInputButton(FileInputButtonBase):
    """
    FileInputButtonBase version which includes the required assets to customize
    its layout and turn the file input as a button.
    """
    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/fileinputbutton.css",),
        }
        js = ("cmsplugin_blocks/js/fileinputbutton.js",)


class ClearableFileInputButton(ClearableFileInputButtonBase):
    """
    ClearableFileInputButtonBase version which includes the required assets to
    customize its layout and turn the file input as a button.
    """
    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/fileinputbutton.css",),
        }
        js = ("cmsplugin_blocks/js/fileinputbutton.js",)
