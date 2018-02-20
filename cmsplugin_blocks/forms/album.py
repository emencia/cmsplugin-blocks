# -*- coding: utf-8 -*-
import zipfile

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from djangocms_text_ckeditor.widgets import TextEditorWidget

from cmsplugin_blocks.models.album import Album, AlbumItem
from cmsplugin_blocks.utils import store_images_from_zip


class AlbumItemForm(forms.ModelForm):
    class Meta:
        model = AlbumItem
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
        Validate uploaded ZIP archive file and temporary store it in
        'uploaded_zip' form object attribute if valid
        """
        data = self.cleaned_data['mass_upload']

        if data:
            # Validate ZIP from file metas first octets
            if not zipfile.is_zipfile(data):
                raise forms.ValidationError("Submited file is not a ZIP archive file")

            # Open ZIP
            archive = zipfile.ZipFile(data)

            # Search for corrupted files
            corrupted_file = archive.testzip()
            if corrupted_file:
                raise forms.ValidationError("File '{}' in ZIP archive is corrupted".format(corrupted_file))

            # ZIP is totally ok, store it to attribute
            self.uploaded_zip = archive

        return data

    def save(self, *args, **kwargs):
        album = super(AlbumForm, self).save(*args, **kwargs)

        # Collect item from zip if any
        items = store_images_from_zip(album, self.uploaded_zip, AlbumItem, 'album', 'image')

        return album

    class Meta:
        model = Album
        fields = [
            'title',
            'template',
            'mass_upload',
        ]
        exclude = []
