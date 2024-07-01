from django.db import models
from django.core.exceptions import ValidationError
from django.forms import MultipleChoiceField


class CommaSeparatedStringsField(models.CharField):
    """
    A custom model field to store and manage a list of words in a varchar using input
    "MultipleChoiceField".

    This enable to store a list of items without to goes through a M2M relation for
    nothing.

    Words are separated with a comma so comma in a word is forbidden, you may need
    to define a validator to avoid it from choice values.

    This field is compatible with widgets:

    * ``django.forms.SelectMultiple`` (default)
    * ``django.forms.CheckboxSelectMultiple``
    * ``django.contrib.admin.widgets.FilteredSelectMultiple``

    .. NOTE::
        Grouped choices are not supported.

    """
    def from_db_value(self, value, *args):
        """
        Decompress the value to a list.
        """
        if not value:
            return []

        return value.split(",")

    def get_prep_value(self, value):
        """
        Compress the value to a string with comma as item divider.
        """
        return ",".join(value)

    def to_python(self, value):
        """
        Give the value to use by formfield and its widget.
        """
        if isinstance(value, list):
            return value

        return self.from_db_value(value)

    def value_to_string(self, obj):
        """
        Convert value (as given by formfield and its widget) as it will be stored.
        """
        return self.get_prep_value(self.value_from_object(obj))

    def formfield(self, **kwargs):
        """
        Define the right formfield to use.

        .. NOTE::
            This is ignored from ModelAdmin, you will need to enforce it in your admin
            form.
        """
        defaults = {"form_class": MultipleChoiceField}
        defaults.update(kwargs)

        return models.Field.formfield(self, **defaults)

    def validate(self, value, model_instance):
        """
        Override the default Field validation for choices since default implementation
        (from ``db.models.fields.Field``) expect a simple string value but we are
        using a list of string from ``MultipleChoiceField``.
        """
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if self.choices is not None and value not in self.empty_values:
            choices_values = [k for k, v in self.choices]

            # Value is expected to be a list
            for item in value:
                # Check value item is a valid choice
                if item not in choices_values:
                    raise ValidationError(
                        self.error_messages["invalid_choice"],
                        code="invalid_choice",
                        params={"value": item},
                    )

        if value is None and not self.null:
            raise ValidationError(self.error_messages["null"], code="null")

        if not self.blank and value in self.empty_values:
            raise ValidationError(self.error_messages["blank"], code="blank")
