from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
import datetime

from django.views.generic import View

from .. import __version__
from ..models import Feature
# from ..forms import FeatureImportForm

from .admin_mixins import CustomAdminContext


class FeatureExportAdminView(View):
    """
    Mixin to display a form to select a language to translate an object to.

    The form does not perform a POST request. Instead it will make a GET to the object
    create form with some URL argument so the create form will know it will have to
    prefill fields "language" and "original", the user still have to fill everything
    else.

    Form only displays the language which are still available (not in original and
    its possible translations).

    Given ID is used to retrieve an object and get its original if its
    translation. Finally the form will always redirect to an original object.

    Despite inheriting from DetailView, this is not a ready to use view, you need
    inherit it to define the ``mode`` and ``template_name`` attributes correctly.
    """
    model = Feature
    context_object_name = "requested_object"
    http_method_names = ["get", "head", "options", "trace"]

    def get_queryset(self):
        return self.model.objects.all().order_by("scope")

    def get_items(self):
        return list(self.get_queryset().values(
            "title",
            "value",
            "scope",
            "plugins",
        ))

    def get(self, request):
        return JsonResponse(
            {
                "version":  __version__,
                "date": datetime.datetime.now().isoformat(timespec="seconds"),
                "items": self.get_items(),
            },
            json_dumps_params={"indent": 4},
        )
