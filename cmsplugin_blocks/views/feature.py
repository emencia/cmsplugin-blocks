import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View, FormView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .. import __version__
from ..models import Feature
from ..forms import FeatureImportForm
from .admin_mixins import CustomAdminContext


class FeatureExportAdminView(View):
    """
    View to export all existing features into a JSON dump.

    This is a basic view with a simple JSON response that would look like this: ::

        {
            "version": "1.3.0",
            "date": "2024-07-05T15:04:21",
            "items": [
                {
                    "title": "DANGER",
                    "value": "bg-danger",
                    "scope": "color",
                    "plugins": [
                        "AlbumMain",
                        "CardMain"
                    ]
                }
            ]
        }

    Items ``version`` and ``items`` are required, ``date`` is optional but may be
    useful when storing some common dump.

    Item ``version`` is currently not used but may be so in future version to manage
    possible incompatibility.

    Item ``items`` is a list of dictionnary for feature items to load. All feature item
    fields are required and must not be empty.
    """
    model = Feature
    http_method_names = ["get", "head", "options", "trace"]

    def get_queryset(self):
        return self.model.objects.all().order_by("scope", "title")

    def get(self, request):
        """
        Return built JSON content from features.
        """
        return JsonResponse(
            {
                "version":  __version__,
                "date": datetime.datetime.now().isoformat(timespec="seconds"),
                "items": self.get_queryset().get_payload(),
            },
            json_dumps_params={"indent": 4},
        )


class FeatureImportAdminView(CustomAdminContext, FormView):
    """
    View to import Feature items from a JSON file.

    Expected JSON format is the same as described in ``FeatureExportAdminView``.
    """
    model = Feature
    form_class = FeatureImportForm
    template_name = "admin/cmsplugin_blocks/feature/import.html"
    title = _("Import features")
    success_url = reverse_lazy("admin:cmsplugin_blocks_feature_changelist")

    def form_valid(self, form):
        """
        When form validation has succeeded, save dump items, save a success
        notification then redirect to change list.
        """
        results = form.save()

        success_message = self.get_success_message(results)
        if success_message:
            messages.success(self.request, success_message)

        return super().form_valid(form)

    def get_success_message(self, results):
        """
        Build success message from result stats.

        Arguments:
            results (dict): Dictionnary of results stats as returned from
                ``FeatureImportForm.save()``.

        Returns:
            string: The success message may be composed of created, ignored per scope
            and ignored duplicates parts, depending they are empty or not.
        """
        parts = []

        created_msg = _("{count} items have been created")
        ignored_msg = _("{count} items have been ignored from scopes ({scopes})")
        duplicates_msg = _("{count} items were duplicated titles")

        if len(results["created"]) > 0:
            parts.append(
                created_msg.format(count=len(results["created"]))
            )

        if len(results["ignored"]) > 0:
            parts.append(
                ignored_msg.format(
                    count=len(results["ignored"]),
                    scopes=", ".join(results["disallowed_scopes"]),
                )
            )

        if len(results["duplicates"]) > 0:
            parts.append(
                duplicates_msg.format(count=len(results["duplicates"]))
            )

        return ". ".join(parts)
