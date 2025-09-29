"""
Admin configuration for comercial models.
"""

from django.contrib import admin
from ncc_school_management.admin import make_active, make_inactive, soft_delete_selected
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """
    list_display = ["name", "price", "duration_months", "is_active", "created_at"]
    list_filter = ["is_active", "created_at", "updated_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["name"]
    list_per_page = 20
    actions = [make_active, make_inactive, soft_delete_selected]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "description", "is_active")
        }),
        ("Pricing & Duration", {
            "fields": ("price", "duration_months")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )
