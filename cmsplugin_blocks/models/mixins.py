from django.utils.functional import cached_property

from .feature import Feature


class FeatureMixinModel:
    """
    A mixin to inherit useful methods in model which implement features.

    This is not a abstract model, the related fields will have to be in your model: ::

        size_features = models.ManyToManyField(
            "cmsplugin_blocks.Feature",
            verbose_name=_("size features"),
            related_name="%(app_label)s_%(class)s_size_related",
            blank=True,
            limit_choices_to={"scope": "size", "plugins__contains": NAME},
        )

        color_features = models.ManyToManyField(
            "cmsplugin_blocks.Feature",
            verbose_name=_("color features"),
            related_name="%(app_label)s_%(class)s_color_related",
            blank=True,
            limit_choices_to={"scope": "color", "plugins__contains": NAME},
        )

        extra_features = models.ManyToManyField(
            "cmsplugin_blocks.Feature",
            verbose_name=_("extra features"),
            related_name="%(app_label)s_%(class)s_extra_related",
            blank=True,
            limit_choices_to={"scope": "extra", "plugins__contains": NAME},
        )

    Where ``NAME`` is the key name to use to limit choices, this name is a model name
    and must exists in ``settings.BLOCKS_KNOWED_FEATURES_PLUGINS``.
    """
    def copy_relations(self, oldinstance):
        """
        Copy all relations when plugin object is copied as another object.

        See:

        https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html#relations-between-plugins

        .. Warning:
            Plugin models may need to call this method (with ``super()`` when they have
            over relation to copy (like Album or Slider) since this mixin method is
            only about m2m feature fields.
        """
        self.size_features.set(oldinstance.size_features.all())
        self.color_features.set(oldinstance.color_features.all())
        self.extra_features.set(oldinstance.extra_features.all())

    def query_size_features(self):
        """
        Build queryset for listing 'size' features.

        Scope and allowed plugin are enforced in queryset lookups.

        Returns:
            Queryset: A 'value_list' queryset of features.
        """
        queryset = self.size_features.filter(
            scope="size",
            plugins__contains=self.__class__.__name__,
        )
        return queryset.query_minimal_payload()

    def query_color_features(self):
        """
        Build queryset for listing 'color' features.

        Scope and allowed plugin are enforced in queryset lookups.

        Returns:
            Queryset: A 'value_list' queryset of features.
        """
        queryset = self.color_features.filter(
            scope="color",
            plugins__contains=self.__class__.__name__,
        )
        return queryset.query_minimal_payload()

    def query_extra_features(self):
        """
        Build queryset for listing 'extra' features.

        Scope and allowed plugin are enforced in queryset lookups.

        Returns:
            Queryset: A 'value_list' queryset of features.
        """
        queryset = self.extra_features.filter(
            scope="extra",
            plugins__contains=self.__class__.__name__,
        )
        return queryset.query_minimal_payload()

    @cached_property
    def query_features(self):
        """
        Build queryset for listing all scope features.

        This is a cached property so you may use it multiple time on the same object
        session and it will only perform queryset request once. This is a memory cache
        not a proper cache as from Django’s cache framework.

        Returns:
            Queryset: A 'value_list' queryset of features.
        """
        sizes = self.query_size_features()
        colors = self.query_color_features()
        extras = self.query_extra_features()

        # Join results from queryset unions
        return extras.union(sizes, colors)

    def scoped_features(self):
        """
        Return a structured data of feature items per scope.

        Returns:
            dict: Dictionnary where each key is a scope and associated value is a list
            of string for feature value. Scope without any item is still present but
            as an empty list.

            Example: ::
                >>> some_object_with_features.scoped_features()

                {
                    "size": ["bar", "foo"],
                    "color": [],
                    "extra": ["foo", "ping"],
                }
        """
        # Join results from queryset unions
        parts = list(self.query_features)

        # Index values on their scope
        return {
            k: sorted([feature["value"] for feature in parts if k == feature["scope"]])
            for k, v in Feature.SCOPE_CHOICES
        }

    def flat_features(self):
        """
        Merge features items into a single string with a whitespace divider.

        Returns:
            string: Feature items divided by a whitespace. This enforce classnames
            uniqueness.

            Example: ::
                >>> some_object_with_features.flat_features()

                "bar foo ping"
        """
        # Join results from queryset unions
        parts = " ".join([item["value"] for item in self.query_features])

        # Split again classnames to remove duplicate and reorder
        return " ".join(sorted(set(parts.split())))
