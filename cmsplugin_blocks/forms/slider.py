from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..models.slider import Slider, SlideItem


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        exclude = []
        fields = [
            "title",
            "template",
            "size_features",
            "color_features",
            "extra_features",
        ]
        widgets = {
            "size_features": forms.CheckboxSelectMultiple,
            "color_features": forms.CheckboxSelectMultiple,
            "extra_features": forms.CheckboxSelectMultiple,
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/slider.css",),
        }


class SlideItemForm(forms.ModelForm):
    class Meta:
        model = SlideItem
        exclude = []
        fields = [
            "slider",
            "title",
            "order",
            "image",
            "image_alt",
            "content",
            "link_name",
            "link_url",
            "link_open_blank",
        ]
        widgets = {
            "content": TextEditorWidget,
        }
