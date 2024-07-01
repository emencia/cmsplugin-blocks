from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..choices_helpers import get_card_feature_choices
from ..models.card import Card


class CardForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_card_feature_choices(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name=None, is_stacked=False),
        # widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Card
        exclude = []
        fields = [
            "title",
            "template",
            "features",
            "image",
            "image_alt",
            "content",
            "link_url",
            "link_open_blank",
        ]
        widgets = {
            "content": TextEditorWidget,
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/card.css",),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get back original model field name onto the field
        self.fields["features"].label = (
            self._meta.model._meta.get_field("features").verbose_name
        )
