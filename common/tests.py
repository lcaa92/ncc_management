"""
Tests for common models and mixins.
"""

import pytest
from django.test import TestCase
from django.utils import timezone
from django.db import models

from .models import TimestampMixin, SoftDeleteMixin, BaseModel


class TestModel(TimestampMixin, SoftDeleteMixin, models.Model):
    """
    Test model for testing mixins.
    """
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "common"
        db_table = "common_test_model"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TimestampMixinTest(TestCase):
    """
    Test cases for TimestampMixin.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.test_model = TestModel.objects.create(name="Test")

    def test_created_at_auto_set(self):
        """
        Test that created_at is automatically set.
        """
        self.assertIsNotNone(self.test_model.created_at)
        self.assertIsInstance(self.test_model.created_at, timezone.datetime)

    def test_updated_at_auto_set(self):
        """
        Test that updated_at is automatically set.
        """
        self.assertIsNotNone(self.test_model.updated_at)
        self.assertIsInstance(self.test_model.updated_at, timezone.datetime)

    def test_updated_at_changes_on_save(self):
        """
        Test that updated_at changes when the model is saved.
        """
        original_updated_at = self.test_model.updated_at
        self.test_model.name = "Updated Test"
        self.test_model.save()
        self.assertGreater(self.test_model.updated_at, original_updated_at)


class SoftDeleteMixinTest(TestCase):
    """
    Test cases for SoftDeleteMixin.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.test_model = TestModel.objects.create(name="Test")

    def test_soft_delete_sets_deleted_at(self):
        """
        Test that soft delete sets deleted_at timestamp.
        """
        self.assertIsNone(self.test_model.deleted_at)
        self.test_model.delete()
        self.assertIsNotNone(self.test_model.deleted_at)
        self.assertIsInstance(self.test_model.deleted_at, timezone.datetime)

    def test_is_deleted_property(self):
        """
        Test the is_deleted property.
        """
        self.assertFalse(self.test_model.is_deleted)
        self.test_model.delete()
        self.assertTrue(self.test_model.is_deleted)

    def test_hard_delete_removes_from_db(self):
        """
        Test that hard_delete removes the record from the database.
        """
        model_id = self.test_model.id
        self.test_model.hard_delete()
        with self.assertRaises(TestModel.DoesNotExist):
            TestModel.objects.get(id=model_id)


class BaseModelTest(TestCase):
    """
    Test cases for BaseModel.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.test_model = TestModel.objects.create(name="Test")

    def test_inherits_timestamp_mixin(self):
        """
        Test that BaseModel inherits from TimestampMixin.
        """
        self.assertIsNotNone(self.test_model.created_at)
        self.assertIsNotNone(self.test_model.updated_at)

    def test_inherits_soft_delete_mixin(self):
        """
        Test that BaseModel inherits from SoftDeleteMixin.
        """
        self.assertIsNone(self.test_model.deleted_at)
        self.test_model.delete()
        self.assertIsNotNone(self.test_model.deleted_at)
