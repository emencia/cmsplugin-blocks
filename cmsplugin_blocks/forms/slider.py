# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.slider import Slider, SlideItem
from cmsplugin_blocks.widgets import ClearableFileInputButtonBase


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = [
            "title",
            "template",
        ]
        exclude = []

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/slider.css",),
        }
        js = ("cmsplugin_blocks/js/fileinputbutton.js",)


class SlideItemForm(forms.ModelForm):
    class Meta:
        model = SlideItem
        widgets = {
            "image": ClearableFileInputButtonBase,
            "content": TextEditorWidget,
        }
        fields = [
            "slider",
            "title",
            "image",
            "content",
            "order",
            "link_name",
            "link_url",
            "link_open_blank",
        ]
        exclude = []
