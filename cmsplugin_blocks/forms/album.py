# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.album import Album, AlbumItem


class AlbumItemForm(forms.ModelForm):
    class Meta:
        model = AlbumItem
        widgets = {
            'content': TextEditorWidget,
        }
        fields = [
            'album',
            'image',
            'content',
        ]
        exclude = []


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        widgets = {
            'brief': TextEditorWidget,
        }
        fields = [
            'title',
            'brief',
            'template',
        ]
        exclude = []
