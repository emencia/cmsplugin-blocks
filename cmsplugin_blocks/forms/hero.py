# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.hero import Hero


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        widgets = {
            'content': TextEditorWidget,
        }
        fields = [
            'template',
            'image',
            'content',
        ]
        exclude = []
