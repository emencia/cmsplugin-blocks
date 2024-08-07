from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from ..models.accordion import Accordion, AccordionItem


class AccordionForm(forms.ModelForm):
    class Meta:
        model = Accordion
        exclude = []
        fields = [
            "title",
            "template",
            "size_features",
            "color_features",
            "extra_features",
        ]
        widgets = {
            "size_features": forms.CheckboxSelectMultiple,
            "color_features": forms.CheckboxSelectMultiple,
            "extra_features": forms.CheckboxSelectMultiple,
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/slider.css",),
        }


class AccordionItemForm(forms.ModelForm):
    class Meta:
        model = AccordionItem
        exclude = []
        fields = [
            "accordion",
            "title",
            "order",
            "image",
            "image_alt",
            "content",
        ]
        widgets = {
            "content": TextEditorWidget,
        }