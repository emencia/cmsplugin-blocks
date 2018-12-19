# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.slider import Slider, SlideItem


class SlideItemForm(forms.ModelForm):
    class Meta:
        model = SlideItem
        widgets = {
            'content': TextEditorWidget,
        }
        fields = [
            'slider',
            'image',
            'content',
            'order',
            'link_name',
            'link_url',
            'link_open_blank',
        ]
        exclude = []


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = [
            'title',
            'template',
        ]
        exclude = []
