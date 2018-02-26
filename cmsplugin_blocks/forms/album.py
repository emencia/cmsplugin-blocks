# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import FileInput, NumberInput

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.album import Album, AlbumItem
from cmsplugin_blocks.utils import (validate_file_size, validate_zip,
                                    store_images_from_zip)


class AlbumItemForm(forms.ModelForm):
    class Meta:
        model = AlbumItem
        widgets = {
            'image': FileInput,
            'order': NumberInput(attrs={'style': 'width: 80px !important;'}),
        }
        fields = [
            'album',
            'title',
            'order',
            'image',
        ]
        exclude = []


class AlbumForm(forms.ModelForm):
    mass_upload = forms.FileField(
        label=_('Add items from a ZIP file'),
        max_length=100,
        required=False,
        help_text=_("Select a '*.zip' file of images to upload as new items.")
    )

    def __init__(self, *args, **kwargs):
        self.uploaded_zip = None

        super(AlbumForm, self).__init__(*args, **kwargs)


    def clean_mass_upload(self):
        """
        Validate uploaded ZIP archive file and temporary store it to
        'uploaded_zip' form object attribute if valid.
        """
        data = self.cleaned_data['mass_upload']

        if data:
            validate_file_size(data)
            validate_zip(data, obj=self)

        return data

    def save(self, *args, **kwargs):
        album = super(AlbumForm, self).save(*args, **kwargs)

        # Collect item from zip if any
        album._awaiting_items = store_images_from_zip(
            album,
            self.uploaded_zip,
            AlbumItem,
            'album',
            'image',
            label_attrname="title"
        )

        return album

    class Meta:
        model = Album
        fields = [
            'title',
            'template',
            'mass_upload',
        ]
        exclude = []
