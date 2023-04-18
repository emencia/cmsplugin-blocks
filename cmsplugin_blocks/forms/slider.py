from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..choices_helpers import (
    get_slider_feature_choices,
    get_slideritem_feature_choices,
)
from ..models.slider import Slider, SlideItem


class SliderForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_slider_feature_choices(),
        required=False,
    )

    class Meta:
        model = Slider
        exclude = []
        fields = [
            "title",
            "template",
            "features",
        ]
        widgets = {
            "features": forms.SelectMultiple,
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/slider.css",),
        }


class SlideItemForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_slideritem_feature_choices(),
        required=False,
    )

    class Meta:
        model = SlideItem
        exclude = []
        fields = [
            "slider",
            "title",
            "features",
            "order",
            "image",
            "content",
            "link_name",
            "link_url",
            "link_open_blank",
        ]
        widgets = {
            "content": TextEditorWidget,
            "features": forms.SelectMultiple,
        }
