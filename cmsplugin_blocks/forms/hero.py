from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..models.hero import Hero


class HeroForm(forms.ModelForm):
    """
    Hero form used in plugin editor.
    """
    class Meta:
        model = Hero
        exclude = []
        fields = [
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
            "all": ("cmsplugin_blocks/css/admin/hero.css",),
        }
