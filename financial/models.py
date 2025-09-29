"""
Financial models for the NCC School Management system.
"""

from django.db import models
from django.core.validators import MinValueValidator
from common.models import BaseModel


class PaymentMethod(models.TextChoices):
    """
    Enum for payment methods.
    """
    CREDIT_CARD = "credit_card", "Credit Card"
    PIX = "pix", "PIX"
    BOLETO = "boleto", "Boleto"


class Payment(BaseModel):
    """
    Payment model representing individual payments.
    """
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        help_text="Method used for the payment"
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Amount paid in local currency"
    )
    paid_at = models.DateTimeField(
        help_text="Timestamp when the payment was completed"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Description or reference for the payment"
    )

    class Meta:
        db_table = "financial_payments"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-paid_at"]

    def __str__(self):
        return f"Payment of {self.value} via {self.get_payment_method_display()}"


class TeacherPayments(BaseModel):
    """
    Teacher payments model for tracking teacher compensation.
    """
    teacher = models.ForeignKey(
        "management.Teacher",
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="Teacher who received the payment"
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Amount paid to the teacher in local currency"
    )
    paid_at = models.DateTimeField(
        help_text="Timestamp when the payment was completed"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        help_text="Method used for the payment"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Description or reference for the payment"
    )

    class Meta:
        db_table = "financial_teacher_payments"
        verbose_name = "Teacher Payment"
        verbose_name_plural = "Teacher Payments"
        ordering = ["-paid_at"]

    def __str__(self):
        return f"Payment to {self.teacher.name}: {self.value} via {self.get_payment_method_display()}"
