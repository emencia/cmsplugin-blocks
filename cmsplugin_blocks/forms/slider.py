from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

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
        widget=FilteredSelectMultiple(verbose_name=None, is_stacked=False),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get back original model field name onto the field
        self.fields["features"].label = (
            self._meta.model._meta.get_field("features").verbose_name
        )


class SlideItemForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_slideritem_feature_choices(),
        required=False,
        widget=forms.SelectMultiple,
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
            "image_alt",
            "content",
            "link_name",
            "link_url",
            "link_open_blank",
        ]
        widgets = {
            "content": TextEditorWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get back original model field name onto the field
        self.fields["features"].label = (
            self._meta.model._meta.get_field("features").verbose_name
        )
