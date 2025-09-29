"""
Admin configuration for CRM models.
"""

from django.contrib import admin
from ncc_school_management.admin import soft_delete_selected
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """
    Admin configuration for Lead model.
    """
    list_display = ["name", "email", "phone", "birth_date", "created_at"]
    list_filter = ["birth_date", "created_at", "updated_at"]
    search_fields = ["name", "email", "phone", "goals", "interests"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["-created_at"]
    list_per_page = 20
    actions = [soft_delete_selected]

    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "birth_date", "email", "phone")
        }),
        ("Goals & Interests", {
            "fields": ("goals", "interests")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )
