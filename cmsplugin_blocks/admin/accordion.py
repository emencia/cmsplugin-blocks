from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from smart_media.admin import SmartModelAdmin

from ..forms.accordion import AccordionItemForm
from ..models.accordion import AccordionItem


class AccordionItemAdmin(admin.StackedInline):
    """
    Plugin admin form to enable inline mode inside AccordionPlugin
    """
    model = AccordionItem
    form = AccordionItemForm
    extra = 0
    verbose_name = _("Accordion")
    ordering = ["order"]
    formfield_overrides = SmartModelAdmin.formfield_overrides

    def get_fieldsets(self, request, obj=None):
        """
        Define plugin form fieldsets depending features are enabled or not (when there
        is no defined feature choices).
        """
        fieldsets = [
            (None, {
                "fields": (
                    "accordion",
                ),
            }),
            (_("Content"), {
                "fields": (
                    "title",
                    "image",
                    "content",
                ),
            }),
            (_("Options"), {
                "fields": (
                    "order",
                    "opened",
                    "image_alt",
                ),
            }),
        ]

        return tuple(fieldsets)
