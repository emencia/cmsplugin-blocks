from django.db import models


class FeatureQuerySet(models.QuerySet):
    def get_payload(self):
        """
        Return a list of item as dictionnary from current queryset.

        Since it does not return a queryset you cannot chain it with following lookup
        filters, this is a terminal queryset. Also, it needs a basic queryset before
        to be used, a ``all()`` filter will be enough.

        Returns:
            list: List of dictionnaries.
        """
        return list(self.values(
            "title",
            "value",
            "scope",
            "plugins",
        ))


class FeatureManager(models.Manager):
    """
    Feature objects manager.
    """
    def get_queryset(self):
        return FeatureQuerySet(self.model, using=self._db)
