# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.diptych import Diptych


class DiptychForm(forms.ModelForm):
    class Meta:
        model = Diptych
        widgets = {
            'content': TextEditorWidget,
        }
        fields = [
            'alignment',
            'image',
            'content',
        ]
        exclude = []
