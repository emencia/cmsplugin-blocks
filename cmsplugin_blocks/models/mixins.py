
class FeatureMixinModel:
    """
    A mixin to inherit in model which implement features.

    This is not a abstract model, the related fields will have to be in your model: ::

        size_features = models.ManyToManyField(
            "cmsplugin_blocks.Feature",
            verbose_name=_("size features"),
            related_name="%(app_label)s_%(class)s_size_related",
            blank=True,
            limit_choices_to={"scope": "size", "plugins__contains": "PLUGIN NAME"},
        )

        color_features = models.ManyToManyField(
            "cmsplugin_blocks.Feature",
            verbose_name=_("color features"),
            related_name="%(app_label)s_%(class)s_color_related",
            blank=True,
            limit_choices_to={"scope": "color", "plugins__contains": "PLUGIN NAME"},
        )

        extra_features = models.ManyToManyField(
            "cmsplugin_blocks.Feature",
            verbose_name=_("extra features"),
            related_name="%(app_label)s_%(class)s_extra_related",
            blank=True,
            limit_choices_to={"scope": "extra", "plugins__contains": "PLUGIN NAME"},
        )

    Where ``PLUGIN NAME`` is the key name to use to limit choices, this name must
    exists in ``settings.BLOCKS_FEATURE_PLUGINS``.
    """

    def get_size_features(self):
        """
        Build queryset for listing size feature values.

        Returns:
            Queryset: A 'value_list' queryset of features.
        """
        return self.size_features.all().values_list("value", flat=True)

    def get_color_features(self):
        """
        Build queryset for listing color feature values.

        Returns:
            Queryset: A 'value_list' queryset of features.
        """
        return self.color_features.all().values_list("value", flat=True)

    def get_extra_features(self):
        """
        Build queryset for listing extra feature values.

        Returns:
            Queryset: A 'value_list' queryset of features.
        """
        return self.extra_features.all().values_list("value", flat=True)

    def get_features(self):
        """
        Merge features items into a single string with a whitespace divider.

        Returns:
            string: Feature items divided by a whitespace. This enforce classnames
            uniqueness.
        """
        sizes = self.get_size_features()
        colors = self.get_color_features()
        extras = self.get_extra_features()
        # Join results from queryset unions
        parts = " ".join(extras.union(sizes, colors))
        # Split again classnames to remove duplicate and reorder
        return " ".join(sorted(set(parts.split())))

    def copy_relations(self, oldinstance):
        """
        Copy all relations when plugin object is copied as another object.

        See:

        https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html#relations-between-plugins

        .. Warning:
            Plugin models may need to inherit this method when they have over relation
            to copy since this mixin method is only about m2m feature fields.
        """
        self.size_features.set(oldinstance.size_features.all())
        self.color_features.set(oldinstance.color_features.all())
        self.extra_features.set(oldinstance.extra_features.all())
