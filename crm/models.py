"""
CRM models for the NCC School Management system.
"""

from django.db import models
from common.models import BaseModel


class Lead(BaseModel):
    """
    Lead model representing potential students or customers.
    """
    name = models.CharField(
        max_length=255,
        help_text="Full name of the lead"
    )
    goals = models.TextField(
        help_text="Goals and objectives of the lead"
    )
    birth_date = models.DateField(
        help_text="Date of birth of the lead"
    )
    interests = models.TextField(
        blank=True,
        null=True,
        help_text="Areas of interest or specific courses the lead is interested in"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email address of the lead"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Phone number of the lead"
    )

    class Meta:
        db_table = "crm_leads"
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
