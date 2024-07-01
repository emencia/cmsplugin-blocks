from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import NumberInput
from django.utils.translation import gettext_lazy as _

from smart_media.widgets import FileInputButtonBase

from ..choices_helpers import (
    get_album_feature_choices,
    get_albumitem_feature_choices,
)
from ..models.album import Album, AlbumItem
from ..utils import (
    validate_file_size,
    validate_zip,
    store_images_from_zip,
)


class AlbumForm(forms.ModelForm):
    """
    Form to manage an Album with possible ZIP file to store items.

    Be aware that this form does not finally save collected image items, they
    are stored to attribute ``_awaiting_items`` on Album instance. Then in the
    common workflow, the CMS plugin using this form will get this attribute and
    perform final save. If you use this form without the CMS plugin edit
    workflow, you will need to reproduce it.
    """

    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_album_feature_choices(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name=None, is_stacked=False),
    )

    mass_upload = forms.FileField(
        label=_("Add items from a ZIP"),
        max_length=100,
        required=False,
        help_text=_("Select a '*.zip' file of images to upload as new items."),
        widget=FileInputButtonBase,
    )

    class Meta:
        model = Album
        exclude = []
        fields = [
            "title",
            "template",
            "features",
            "mass_upload",
        ]
        widgets = {
            "order": NumberInput(attrs={"style": "width: 80px !important;"}),
        }

    class Media:
        css = {
            "all": ("cmsplugin_blocks/css/admin/album.css",),
        }

    def __init__(self, *args, **kwargs):
        self.uploaded_zip = None

        super().__init__(*args, **kwargs)

        # Get back original model field name onto the field
        self.fields["features"].label = (
            self._meta.model._meta.get_field("features").verbose_name
        )

    def clean_mass_upload(self):
        """
        Validate uploaded ZIP archive file and temporary store it to
        "uploaded_zip" form object attribute if valid.
        """
        data = self.cleaned_data["mass_upload"]

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
            "album",
            "image",
            label_attrname="title"
        )

        return album


class AlbumItemForm(forms.ModelForm):
    # Enforce the right field since ModelAdmin ignore the formfield defined in custom
    # modelfield. Option have to fit to the modelfield ones.
    features = forms.MultipleChoiceField(
        choices=get_albumitem_feature_choices(),
        required=False,
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = AlbumItem
        exclude = []
        fields = [
            "album",
            "title",
            "order",
            "features",
            "image",
            "image_alt",
        ]
        widgets = {
            "order": NumberInput(attrs={"style": "width: 80px !important;"}),
        }
