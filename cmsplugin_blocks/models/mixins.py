
class FeatureMixinModel:
    """

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
        Merge feature kinds items into a single string with a comma divider.

        Returns:
            string: Feature items divided by a comma.
        """
        sizes = self.get_size_features()
        colors = self.get_color_features()
        extras = self.get_extra_features()

        return " ".join(extras.union(sizes, colors))

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
