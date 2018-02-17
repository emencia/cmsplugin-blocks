# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.card import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        widgets = {
            'content': TextEditorWidget,
        }
        fields = [
            'alignment',
            'template',
            'image',
            'content',
        ]
        exclude = []
