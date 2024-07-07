import json

from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError

from ..models import Feature
from ..choices_helpers import get_feature_plugin_choices


class FeatureForm(forms.ModelForm):
    """
    Admin form to create or change a Feature object.
    """
    plugins = forms.MultipleChoiceField(
        choices=get_feature_plugin_choices(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Feature
        exclude = []
        fields = [
            "title",
            "value",
            "scope",
            "plugins",
        ]


class FeatureImportForm(forms.Form):
    """
    Admin form to choose Feature import options.
    """
    scopes = forms.MultipleChoiceField(
        required=False,
        choices=Feature.SCOPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text=(
            "Selected scopes will be ignored from loaded JSON items and won't be "
            "created as Feature objects."
        ),
    )
    json_file = forms.FileField(
        required=True,
        help_text="A valid feature JSON file.",
    )

    class Meta:
        fields = [
            "scopes",
            "json_file",
        ]

    def clean_json_file(self):
        """
        Open file to validate it as JSON and return its content.

        NOTE: This could have been done more robustly with Python library "schema".
        """
        data = self.cleaned_data["json_file"]

        # Check if a valid JSON
        try:
            payload = json.load(data.open())
        except json.JSONDecodeError as e:
            raise ValidationError("File is not valid JSON: {}".format(str(e)))
        else:
            # Root type must be a JSON dictionnary
            if not isinstance(payload, dict):
                raise ValidationError(
                    "JSON should be a dictionnary not a: {}".format(
                        type(payload).__name__
                    )
                )

            # Item 'items' is required
            if "items" not in payload:
                raise ValidationError(
                    "JSON is missing 'items' item for the feature data"
                )

            # Item 'items' must be a list
            if not isinstance(payload["items"], list):
                raise ValidationError(
                    "Item 'items' must be a list"
                )

            # Check for some errors from items
            error_lines = []
            existing_titles = {k: [] for k, v in Feature.SCOPE_CHOICES}
            for i, feature in enumerate(payload["items"], start=1):
                # Get missing field or empty values from loaded items
                if (
                    not feature.get("title", "") or not feature.get("value", "") or
                    not feature.get("scope", "") or not feature.get("plugins", "")
                ):
                    error_lines.append(str(i))
                # Check we have a knowed scope
                elif feature["scope"] not in [k for k, v in Feature.SCOPE_CHOICES]:
                    error_lines.append(str(i))
                # Check we have only knowed plugin names
                elif len([
                    item
                    for item in feature["plugins"]
                    if item not in settings.BLOCKS_KNOWED_FEATURES_PLUGINS
                ]) > 0:
                    error_lines.append(str(i))
                # Check for duplicate title per scope
                elif feature["title"] in existing_titles[feature["scope"]]:
                    error_lines.append(str(i))
                # Everything is ok, store title as an existing one for its scope
                else:
                    existing_titles[feature["scope"]].append(feature["title"])

            # Raise error in case of any missing or empty items
            if error_lines:
                raise ValidationError(
                    "Some item are invalid: {}".format(", ".join(error_lines))
                )

        return payload

    def save(self, commit=True):
        """
        Save elligible items from loaded JSON as feature objects.

        Arguments:
            commit (boolean): Only save objects if True.

        Returns:
            dict: A dictionnary with items for effectively created and ignored items
            from loaded JSON.
        """
        created = []
        duplicates = []
        ignored = []

        # Fetch existing items
        existing = Feature.objects.all().get_payload()
        existing_titles = {}
        for k, v in Feature.SCOPE_CHOICES:
            existing_titles[k] = [
                item["title"]
                for item in existing
                if item["scope"] == k
            ]

        # Create features from loaded data if they do not already exists (based on
        # their title)
        for feature_data in self.cleaned_data["json_file"]["items"]:
            if feature_data["title"] not in existing_titles[feature_data["scope"]]:
                if feature_data["scope"] in self.cleaned_data["scopes"]:
                    ignored.append(feature_data)
                else:
                    new_item = Feature(**feature_data)
                    new_item.full_clean()
                    if commit:
                        new_item.save()
                    created.append(feature_data)
            else:
                duplicates.append(feature_data)

        return {
            "disallowed_scopes": self.cleaned_data["scopes"],
            "created": created,
            "duplicates": duplicates,
            "ignored": ignored,
        }
