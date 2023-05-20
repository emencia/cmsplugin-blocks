from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..choices_helpers import get_hero_feature_choices
from ..models.hero import Hero


class HeroForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_hero_feature_choices(),
        required=False,
    )

    class Meta:
        model = Hero
        exclude = []
        fields = [
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
            "all": ("cmsplugin_blocks/css/admin/hero.css",),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get back original model field name onto the field
        self.fields["features"].label = (
            self._meta.model._meta.get_field("features").verbose_name
        )
