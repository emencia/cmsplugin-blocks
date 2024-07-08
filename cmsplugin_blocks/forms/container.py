from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..models.container import Container


class ContainerForm(forms.ModelForm):
    """
    Container form used in plugin editor.
    """
    class Meta:
        model = Container
        exclude = []
        fields = [
            "title",
            "template",
            "image",
            "image_alt",
            "content",
            "size_features",
            "color_features",
            "extra_features",
        ]
        widgets = {
            "content": TextEditorWidget,
            "size_features": forms.CheckboxSelectMultiple,
            "color_features": forms.CheckboxSelectMultiple,
            "extra_features": forms.CheckboxSelectMultiple,
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/container.css",),
        }
