"""
Tests for CRM models.
"""

from django.test import TestCase
from datetime import date

from .models import Lead


class LeadModelTest(TestCase):
    """
    Test cases for Lead model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.lead_data = {
            "name": "John Doe",
            "goals": "Learn Python programming",
            "birth_date": date(2000, 1, 1),
            "interests": "Web development, Data science",
            "email": "john@example.com",
            "phone": "+1234567890",
        }

    def test_create_lead(self):
        """
        Test creating a lead.
        """
        lead = Lead.objects.create(**self.lead_data)
        self.assertEqual(lead.name, "John Doe")
        self.assertEqual(lead.goals, "Learn Python programming")
        self.assertEqual(lead.birth_date, date(2000, 1, 1))
        self.assertEqual(lead.email, "john@example.com")

    def test_lead_str_representation(self):
        """
        Test string representation of Lead.
        """
        lead = Lead.objects.create(**self.lead_data)
        self.assertEqual(str(lead), "John Doe")

    def test_lead_optional_fields(self):
        """
        Test Lead optional fields.
        """
        lead_data_minimal = {
            "name": "Jane Doe",
            "goals": "Learn programming",
            "birth_date": date(1995, 5, 15),
        }
        lead = Lead.objects.create(**lead_data_minimal)
        self.assertEqual(lead.name, "Jane Doe")
        self.assertIsNone(lead.interests)
        self.assertIsNone(lead.email)
        self.assertIsNone(lead.phone)

    def test_lead_soft_delete(self):
        """
        Test Lead soft delete functionality.
        """
        lead = Lead.objects.create(**self.lead_data)
        lead_id = lead.id

        lead.delete()

        # Should still exist in database but with deleted_at set
        self.assertIsNotNone(Lead.objects.all_with_deleted().get(id=lead_id).deleted_at)

        # Should not appear in default queryset
        self.assertFalse(Lead.objects.filter(id=lead_id).exists())

    def test_lead_timestamps(self):
        """
        Test Lead timestamp fields.
        """
        lead = Lead.objects.create(**self.lead_data)
        self.assertIsNotNone(lead.created_at)
        self.assertIsNotNone(lead.updated_at)
