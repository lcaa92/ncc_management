"""
Admin configuration for financial models.
"""

from django.contrib import admin
from ncc_school_management.admin import soft_delete_selected
from .models import Payment, TeacherPayments


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Payment model.
    """
    list_display = ["payment_method", "value", "paid_at", "description", "created_at"]
    list_filter = ["payment_method", "paid_at", "created_at", "updated_at"]
    search_fields = ["description"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["-paid_at"]
    list_per_page = 20
    actions = [soft_delete_selected]

    fieldsets = (
        ("Payment Information", {
            "fields": ("payment_method", "value", "paid_at", "description")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(TeacherPayments)
class TeacherPaymentsAdmin(admin.ModelAdmin):
    """
    Admin configuration for TeacherPayments model.
    """
    list_display = ["teacher", "value", "payment_method", "paid_at", "description", "created_at"]
    list_filter = ["payment_method", "paid_at", "created_at", "updated_at"]
    search_fields = ["teacher__name", "description"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["-paid_at"]
    list_per_page = 20
    actions = [soft_delete_selected]

    fieldsets = (
        ("Payment Information", {
            "fields": ("teacher", "payment_method", "value", "paid_at", "description")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )
