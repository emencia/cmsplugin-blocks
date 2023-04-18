from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..choices_helpers import get_card_feature_choices
from ..models.card import Card


class CardForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_card_feature_choices(),
        required=False,
    )

    class Meta:
        model = Card
        exclude = []
        fields = [
            "title",
            "template",
            "features",
            "image",
            "content",
            "link_url",
            "link_open_blank",
        ]
        widgets = {
            "content": TextEditorWidget,
            "features": forms.SelectMultiple,
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/card.css",),
        }
