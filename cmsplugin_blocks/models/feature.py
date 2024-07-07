from django.db import models
from django.utils.translation import gettext_lazy as _

from ..choices_helpers import get_feature_plugin_choices
from ..modelfields import CommaSeparatedStringsField
from ..utils.validators import validate_css_classname
from ..managers import FeatureManager


class Feature(models.Model):
    """
    Feature model.
    """

    SIZING = "size"
    COLORING = "color"
    EXTRA = "extra"
    SCOPE_CHOICES = [
        (SIZING, "Size"),
        (COLORING, "Color"),
        (EXTRA, "Extra"),
    ]

    title = models.CharField(
        _("title"),
        blank=False,
        max_length=50,
        default="",
    )
    """
    Optional title string.
    """

    value = models.CharField(
        _("value"),
        max_length=100,
        default="",
        validators=[validate_css_classname],
        help_text=_("Valid CSS classname"),
    )
    """
    Number for order position in item list.
    """

    scope = models.CharField(
        _("scope"),
        max_length=50,
        choices=SCOPE_CHOICES,
        default=SIZING,
        help_text=_("The feature scope."),
    )
    """
    Required feature scope choice. (size, color, extra)
    """

    plugins = CommaSeparatedStringsField(
        _("Allowed for plugins"),
        choices=get_feature_plugin_choices(),
        blank=True,
        default="",
        max_length=50,
    )
    """
    Optional string of plugin models names divided by a single comma.
    """

    objects = FeatureManager()

    class Meta:
        verbose_name = _("Layout feature")
        verbose_name_plural = _("Layout Features")
        constraints = [
            models.UniqueConstraint(
                name="blocks_unique_feature_title",
                fields=["scope", "title"],
            ),
        ]

    def __str__(self):
        return "{}:{}".format(self.get_scope_display(), self.title)
