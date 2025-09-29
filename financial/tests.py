"""
Tests for financial models.
"""

import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

from .models import Payment, TeacherPayments, PaymentMethod
from management.models import Teacher


class PaymentModelTest(TestCase):
    """
    Test cases for Payment model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.payment_data = {
            "payment_method": PaymentMethod.PIX,
            "value": Decimal("299.99"),
            "paid_at": timezone.now(),
            "description": "Course payment",
        }

    def test_create_payment(self):
        """
        Test creating a payment.
        """
        payment = Payment.objects.create(**self.payment_data)
        self.assertEqual(payment.payment_method, PaymentMethod.PIX)
        self.assertEqual(payment.value, Decimal("299.99"))
        self.assertEqual(payment.description, "Course payment")

    def test_payment_str_representation(self):
        """
        Test string representation of Payment.
        """
        payment = Payment.objects.create(**self.payment_data)
        expected_str = f"Payment of {payment.value} via {payment.get_payment_method_display()}"
        self.assertEqual(str(payment), expected_str)

    def test_payment_method_choices(self):
        """
        Test PaymentMethod enum choices.
        """
        self.assertEqual(PaymentMethod.CREDIT_CARD, "credit_card")
        self.assertEqual(PaymentMethod.PIX, "pix")
        self.assertEqual(PaymentMethod.BOLETO, "boleto")

    def test_payment_soft_delete(self):
        """
        Test Payment soft delete functionality.
        """
        payment = Payment.objects.create(**self.payment_data)
        payment_id = payment.id

        payment.delete()

        # Should still exist in database but with deleted_at set
        self.assertIsNotNone(Payment.objects.all_with_deleted().get(id=payment_id).deleted_at)

        # Should not appear in default queryset
        self.assertFalse(Payment.objects.filter(id=payment_id).exists())


class TeacherPaymentsModelTest(TestCase):
    """
    Test cases for TeacherPayments model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.teacher = Teacher.objects.create(
            name="John Doe",
            pix_key="john@example.com"
        )
        self.teacher_payment_data = {
            "teacher": self.teacher,
            "value": Decimal("1500.00"),
            "paid_at": timezone.now(),
            "payment_method": PaymentMethod.PIX,
            "description": "Monthly salary",
        }

    def test_create_teacher_payment(self):
        """
        Test creating a teacher payment.
        """
        payment = TeacherPayments.objects.create(**self.teacher_payment_data)
        self.assertEqual(payment.teacher, self.teacher)
        self.assertEqual(payment.value, Decimal("1500.00"))
        self.assertEqual(payment.payment_method, PaymentMethod.PIX)

    def test_teacher_payment_str_representation(self):
        """
        Test string representation of TeacherPayments.
        """
        payment = TeacherPayments.objects.create(**self.teacher_payment_data)
        expected_str = f"Payment to {self.teacher.name}: {payment.value} via {payment.get_payment_method_display()}"
        self.assertEqual(str(payment), expected_str)

    def test_teacher_payment_relationship(self):
        """
        Test TeacherPayments relationship with Teacher.
        """
        payment = TeacherPayments.objects.create(**self.teacher_payment_data)
        self.assertEqual(payment.teacher.name, "John Doe")
        self.assertIn(payment, self.teacher.payments.all())

    def test_teacher_payment_soft_delete(self):
        """
        Test TeacherPayments soft delete functionality.
        """
        payment = TeacherPayments.objects.create(**self.teacher_payment_data)
        payment_id = payment.id

        payment.delete()

        # Should still exist in database but with deleted_at set
        self.assertIsNotNone(TeacherPayments.objects.all_with_deleted().get(id=payment_id).deleted_at)

        # Should not appear in default queryset
        self.assertFalse(TeacherPayments.objects.filter(id=payment_id).exists())
