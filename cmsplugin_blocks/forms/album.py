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
        widgets = {
            'content': TextEditorWidget,
        }
        fields = [
            'album',
            'image',
            'content',
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
            print("clean_mass_upload")
            print(data, type(data))

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
        print("uploaded_zip:", self.uploaded_zip)
        #self.store_images_from_zip(album)
        items = store_images_from_zip(album, self.uploaded_zip, AlbumItem, 'album', 'image')

        return album

    #def store_images_from_zip(self, album):
        #"""
        #Collect every image item from ZIP as AlbumItem linked to a saved Album
        #instance

        #Some code has been taken/inspired from 'models.upload.process_zipfile'
        #from 'imagestore' app.
        #"""
        #stored_items = []

        #if self.uploaded_zip:
            #print("Got a valid ZIP")
            #for filename in sorted(self.uploaded_zip.namelist()):
                ## do not process meta files
                #if filename.startswith('__'):
                    #continue

                #print(filename)

                ## Get archived file from ZIP
                #data = self.uploaded_zip.read(filename)
                #if len(data):
                    #try:
                        ## the following is taken from django.forms.fields.ImageField:
                        ## load() could spot a truncated JPEG, but it loads the entire
                        ## image in memory, which is a DoS vector. See #3848 and #18520.
                        ## verify() must be called immediately after the constructor.
                        #PILImage.open(BytesIO(data)).verify()
                    #except Exception as e:
                        ## if a "bad" file is found we just skip it.
                        #print('Error verifying image: {}'.format(str(e)))
                        #continue

                    #if hasattr(data, 'seek') and isinstance(data.seek, collections.Callable):
                        #print('seeked')
                        #data.seek(0)

                    #try:
                        #item = AlbumItem(album=album)
                        #item.image.save(filename, ContentFile(data))
                        #item.save()
                    #except Exception as e:
                        #print('Error creating item from file: {}'.format(str(e)))
                    #else:
                        #stored_items.append(item)

            ## Drop ZIP file object from memory/tempdir when finished
            #self.uploaded_zip.close()

        #return stored_items

    class Meta:
        model = Album
        widgets = {
            'brief': TextEditorWidget,
        }
        fields = [
            'title',
            'brief',
            'template',
            'mass_upload',
        ]
        exclude = []
