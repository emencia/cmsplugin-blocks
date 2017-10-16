# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models import Cmsplugin_blocks


class Cmsplugin_blocksPluginForm(forms.ModelForm):
    class Meta:
        model = Cmsplugin_blocks
        widgets = {
            'description': TextEditorWidget,
        }
        fields = [
            'title',
            #'image',
            'description',
        ]
        exclude = []
