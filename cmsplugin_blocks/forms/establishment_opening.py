# -*- coding: utf-8 -*-
from django import forms

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.establishment_opening import (
    EstablishmentOpening, DayItem
)


class DayItemForm(forms.ModelForm):
    class Meta:
        model = DayItem
        widgets = {
            'hours': TextEditorWidget,
        }
        fields = [
            'opening',
            'name',
            'hours',
        ]
        exclude = []


class EstablishmentOpeningForm(forms.ModelForm):
    class Meta:
        model = EstablishmentOpening
        widgets = {
            'comment': TextEditorWidget,
        }
        fields = [
            'title',
            'comment',
        ]
        exclude = []
