from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from smart_media.admin import SmartAdminMixin

from ..choices_helpers import (
    get_container_feature_choices,
    get_container_template_default,
)
from ..forms.container import ContainerForm
from ..models.container import Container


class ContainerPlugin(SmartAdminMixin, CMSPluginBase):
    module = _("Blocks")
    name = _("Container")
    model = Container
    form = ContainerForm
    allow_children = True
    render_template = get_container_template_default()
    cache = True

    def get_fieldsets(self, request, obj=None):
        """
        Define plugin form fieldsets depending features are enabled or not (when there
        is no defined feature choices).
        """
        fieldsets = [
            (None, {
                "fields": (
                    "template",
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
                    "image_alt",
                ),
            }),
        ]

        if len(get_container_feature_choices()) > 0:
            fieldsets.append(
                (_("Features"), {
                    "fields": (
                        "features",
                    ),
                }),
            )

        return tuple(fieldsets)

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template

        context.update({
            "instance": instance,
        })

        return context
