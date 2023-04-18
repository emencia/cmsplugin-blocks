from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..choices_helpers import get_container_feature_choices
from ..models.container import Container


class ContainerForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_container_feature_choices(),
        required=False,
    )

    class Meta:
        model = Container
        exclude = []
        fields = [
            "title",
            "template",
            "features",
            "image",
            "content",
        ]
        widgets = {
            "content": TextEditorWidget,
            "features": forms.SelectMultiple,
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/container.css",),
        }
