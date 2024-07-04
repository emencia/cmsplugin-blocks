from django.contrib import admin
from django.conf import settings

from ..models import Feature
from ..forms import FeatureForm


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    form = FeatureForm
    list_display = (
        "title",
        "scope",
        "allowed_plugin_display",
    )
    list_filter = ("scope", "plugins")

    @admin.display(empty_value="None")
    def allowed_plugin_display(self, obj):
        choices = dict(settings.BLOCKS_FEATURE_PLUGINS)
        names = [str(choices[item]) for item in obj.plugins]
        return ", ".join(names)
