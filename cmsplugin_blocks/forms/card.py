# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.card import Card
from cmsplugin_blocks.widgets import ClearableFileInputButtonBase


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        widgets = {
            "image": ClearableFileInputButtonBase,
            "content": TextEditorWidget,
        }
        fields = [
            "alignment",
            "template",
            "image",
            "content",
        ]
        exclude = []

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/card.css",),
        }
        js = ("cmsplugin_blocks/js/fileinputbutton.js",)
