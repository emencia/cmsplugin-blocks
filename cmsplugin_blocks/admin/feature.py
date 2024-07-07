from django.contrib import admin
from django.conf import settings
from django.urls import path

from ..models import Feature
from ..forms import FeatureForm
from ..views.feature import FeatureExportAdminView, FeatureImportAdminView


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """
    Define all Feature model admin options with some additional internal views.
    """
    form = FeatureForm
    change_list_template = "admin/cmsplugin_blocks/feature/change_list.html"
    list_display = ("id", "title", "scope", "value", "allowed_plugin_display")
    list_filter = ("scope", "plugins")
    list_editable = ("title", "value")

    @admin.display(empty_value="None")
    def allowed_plugin_display(self, obj):
        """
        Compile a string of allowed plugins to display in admin list.
        """
        choices = dict(settings.BLOCKS_FEATURE_PLUGINS)
        names = [str(choices[item]) for item in obj.plugins]
        return ", ".join(names)

    def get_urls(self):
        """
        Set some additional custom admin views
        """
        urls = super().get_urls()

        extra_urls = [
            path(
                "export/",
                self.admin_site.admin_view(
                    FeatureExportAdminView.as_view(),
                ),
                name="cmsplugin_blocks_feature_export",
            ),
            path(
                "import/",
                self.admin_site.admin_view(
                    FeatureImportAdminView.as_view(),
                ),
                {"model_admin": self},
                name="cmsplugin_blocks_feature_import",
            ),
        ]

        return extra_urls + urls
