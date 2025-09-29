"""
Common models and mixins for the NCC School Management system.
"""

from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """
    Manager that filters out soft-deleted records by default.
    """
    def get_queryset(self):
        """
        Return queryset excluding soft-deleted records.
        """
        return super().get_queryset().filter(deleted_at__isnull=True)

    def all_with_deleted(self):
        """
        Return queryset including soft-deleted records.
        """
        return super().get_queryset()

    def only_deleted(self):
        """
        Return queryset with only soft-deleted records.
        """
        return super().get_queryset().filter(deleted_at__isnull=False)


class TimestampMixin(models.Model):
    """
    Abstract model that provides created_at and updated_at timestamp fields.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated"
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Abstract model that provides soft delete functionality with deleted_at field.
    """
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the record was soft deleted"
    )

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete the instance by setting deleted_at timestamp.
        """
        self.deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self, using=None, keep_parents=False):
        """
        Permanently delete the instance from the database.
        """
        super().delete(using=using, keep_parents=keep_parents)

    @property
    def is_deleted(self):
        """
        Check if the instance is soft deleted.
        """
        return self.deleted_at is not None


class BaseModel(TimestampMixin, SoftDeleteMixin):
    """
    Base model that combines timestamp and soft delete functionality.
    """
    class Meta:
        abstract = True
