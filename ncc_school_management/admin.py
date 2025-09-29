"""
Custom admin site configuration for NCC School Management.
"""

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, Sum


class NCCAdminSite(AdminSite):
    """
    Custom admin site for NCC School Management.
    """
    site_header = "NCC School Management"
    site_title = "NCC Admin"
    index_title = "Welcome to NCC School Management Administration"

    def get_urls(self):
        """
        Add custom dashboard URL.
        """
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """
        Custom dashboard view with statistics.
        """
        from management.models import Student, Teacher, Contract
        from comercial.models import Product
        from crm.models import Lead
        from financial.models import Payment

        stats = {
            'active_students': Student.objects.filter(status='active').count(),
            'active_teachers': Teacher.objects.filter(status='active').count(),
            'total_products': Product.objects.count(),
            'total_contracts': Contract.objects.count(),
            'total_leads': Lead.objects.count(),
            'total_payments': Payment.objects.count(),
        }

        context = {
            'title': 'Dashboard',
            'stats': stats,
            'has_permission': request.user.has_perm('admin.view_admin'),
        }
        return render(request, 'admin/dashboard.html', context)


# Create custom admin site instance
admin_site = NCCAdminSite(name="ncc_admin")


# Customize the default admin site
admin.site.site_header = "NCC School Management"
admin.site.site_title = "NCC Admin"
admin.site.index_title = "Welcome to NCC School Management Administration"


# Add custom admin actions
@admin.action(description="Mark selected items as active")
def make_active(modeladmin, request, queryset):
    """
    Mark selected items as active.
    """
    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request,
        f"{updated} item(s) were successfully marked as active."
    )


@admin.action(description="Mark selected items as inactive")
def make_inactive(modeladmin, request, queryset):
    """
    Mark selected items as inactive.
    """
    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request,
        f"{updated} item(s) were successfully marked as inactive."
    )


@admin.action(description="Soft delete selected items")
def soft_delete_selected(modeladmin, request, queryset):
    """
    Soft delete selected items.
    """
    count = 0
    for obj in queryset:
        obj.delete()  # This will use our custom soft delete
        count += 1

    modeladmin.message_user(
        request,
        f"{count} item(s) were successfully soft deleted."
    )
