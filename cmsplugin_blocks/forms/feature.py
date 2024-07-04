from django import forms

from ..models import Feature
from ..choices_helpers import get_feature_plugin_choices


class FeatureForm(forms.ModelForm):
    plugins = forms.MultipleChoiceField(
        choices=get_feature_plugin_choices(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Feature
        exclude = []
        fields = [
            "title",
            "value",
            "scope",
            "plugins",
        ]
