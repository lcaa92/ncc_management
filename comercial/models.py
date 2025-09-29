"""
Comercial models for the NCC School Management system.
"""

from django.db import models
from common.models import BaseModel


class Product(BaseModel):
    """
    Product model representing courses or services offered by the school.
    """
    name = models.CharField(
        max_length=255,
        help_text="Name of the product or course"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the product"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price of the product in local currency"
    )
    duration_months = models.PositiveIntegerField(
        help_text="Duration of the product in months"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the product is currently available for enrollment"
    )

    class Meta:
        db_table = "comercial_products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return self.name
