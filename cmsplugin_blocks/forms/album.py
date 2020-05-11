# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import FileInput, NumberInput

from cmsplugin_blocks.models.album import Album, AlbumItem
from cmsplugin_blocks.utils import (validate_file_size, validate_zip,
                                    store_images_from_zip)


class AlbumForm(forms.ModelForm):
    """
    Form to manage an Album with possible ZIP file to store items.

    Be aware that this form does not finally save collected image items, they
    are stored to attribute ``_awaiting_items`` on Album instance. Then in the
    common workflow, the CMS plugin using this form will get this attribute and
    perform final save. If you use this form without the CMS plugin edit
    workflow, you will need to reproduce it.
    """

    mass_upload = forms.FileField(
        label=_('Add items from a ZIP file'),
        max_length=100,
        required=False,
        help_text=_("Select a '*.zip' file of images to upload as new items.")
    )

    def __init__(self, *args, **kwargs):
        self.uploaded_zip = None

        super().__init__(*args, **kwargs)

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
        album = super().save(*args, **kwargs)

        # Collect item from zip if any so final stage code can save them
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
