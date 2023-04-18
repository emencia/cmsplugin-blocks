from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase

from ..choices_helpers import (
    get_container_feature_choices,
    get_container_template_default,
)
from ..forms.container import ContainerForm
from ..models.container import Container


class ContainerPlugin(CMSPluginBase):
    module = _("Blocks")
    name = _("Container")
    model = Container
    form = ContainerForm
    allow_children = True
    render_template = get_container_template_default()
    cache = True

    def get_fieldsets(self, request, obj=None):
        if len(get_container_feature_choices()) > 0:
            fieldsets = (
                (None, {
                    "fields": (
                        "title",
                        "template",
                        (
                            "features",
                            "image",
                        ),
                        "content",
                    ),
                }),
            )
        else:
            fieldsets = (
                (None, {
                    "fields": (
                        "title",
                        "template",
                        "image",
                        "content",
                    ),
                }),
            )

        return fieldsets

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template

        context.update({
            "instance": instance,
        })

        return context
