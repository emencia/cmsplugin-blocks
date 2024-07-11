from django.db import models


class FeatureQuerySet(models.QuerySet):
    def query_full_payload(self):
        """
        Return a queryset of item values with all feature fields except id.

        Returns:
            models.QuerySet: Result queryset.
        """
        return self.values("title", "value", "scope", "plugins")

    def query_minimal_payload(self):
        """
        Return a queryset of item values with feature value and scope only.

        Returns:
            models.QuerySet: Result queryset.
        """
        return self.values("value", "scope")


class FeatureManager(models.Manager):
    """
    Feature objects manager.
    """
    def get_queryset(self):
        return FeatureQuerySet(self.model, using=self._db)
