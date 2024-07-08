from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..models.card import Card


class CardForm(forms.ModelForm):
    """
    Card form used in plugin editor.
    """
    class Meta:
        model = Card
        exclude = []
        fields = [
            "title",
            "template",
            "image",
            "image_alt",
            "content",
            "link_url",
            "link_open_blank",
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
            "all": ("cmsplugin_blocks/css/admin/card.css",),
        }
