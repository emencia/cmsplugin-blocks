from django.contrib import admin


class CustomAdminContext:
    """
    Mixin to add required context for a custom model admin view.

    View using this mixin must have a ``model`` attribute correctly set to your model,
    if your view has no model then this mixin is probably useless.

    Also, there is an optional useful context variable ``title`` to set yourself in
    your view since its value is totally related to the view itself.

    .. Note::
        This mixin won't be enough to use some django admin template like
        ``change_list.html`` since they require a lot more of specific variables.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.request.current_app = "cmsplugin_blocks"

        context.update({
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
            "app_label": self.model._meta.app_label,
            "app_path": self.request.get_full_path(),

        })

        if hasattr(self, "title"):
            context["title"] = self.title

        return context
