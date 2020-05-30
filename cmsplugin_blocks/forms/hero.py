# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.hero import Hero
from cmsplugin_blocks.widgets import ClearableFileInputButtonBase


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        widgets = {
            "image": ClearableFileInputButtonBase,
            "content": TextEditorWidget,
        }
        fields = [
            "template",
            "image",
            "content",
        ]
        exclude = []

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/hero.css",),
        }
        js = ("cmsplugin_blocks/js/fileinputbutton.js",)
