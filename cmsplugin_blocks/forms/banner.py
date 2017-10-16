# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.banner import Banner


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        widgets = {
            'content': TextEditorWidget,
        }
        fields = [
            'background',
            'content',
        ]
        exclude = []
