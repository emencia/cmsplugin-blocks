from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..choices_helpers import get_container_feature_choices
from ..models.container import Container


class ContainerForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_container_feature_choices(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name=None, is_stacked=False),
    )

    class Meta:
        model = Container
        exclude = []
        fields = [
            "title",
            "template",
            "features",
            "image",
            "image_alt",
            "content",
        ]
        widgets = {
            "content": TextEditorWidget,
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/container.css",),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get back original model field name onto the field
        self.fields["features"].label = (
            self._meta.model._meta.get_field("features").verbose_name
        )
