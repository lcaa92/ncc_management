"""
Admin configuration for management models.
"""

from django.contrib import admin
from ncc_school_management.admin import soft_delete_selected
from .models import Student, Teacher, Contract, StudentsGroup, Lesson


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Student model.
    """
    list_display = ["name", "birth_date", "status", "created_at"]
    list_filter = ["status", "birth_date", "created_at", "updated_at"]
    search_fields = ["name", "extra_info"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["name"]
    list_per_page = 20
    actions = [soft_delete_selected]

    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "birth_date", "status")
        }),
        ("Additional Information", {
            "fields": ("extra_info",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """
    Admin configuration for Teacher model.
    """
    list_display = ["name", "status", "pix_key", "created_at"]
    list_filter = ["status", "created_at", "updated_at"]
    search_fields = ["name", "pix_key"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["name"]
    list_per_page = 20
    actions = [soft_delete_selected]

    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "status")
        }),
        ("Payment Information", {
            "fields": ("pix_key",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Admin configuration for Contract model.
    """
    list_display = ["student", "product", "payment_method",
                    "statements", "first_lesson_on", "last_lesson_on", "created_at"]
    list_filter = ["created_at", "updated_at", "first_lesson_on", "last_lesson_on"]
    search_fields = ["student__name", "product__name"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["-created_at"]
    list_per_page = 20
    actions = [soft_delete_selected]

    fieldsets = (
        ("Contract Information", {
            "fields": ("student", "product", "payment_method",
                       "statements", "first_lesson_on", "last_lesson_on")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(StudentsGroup)
class StudentsGroupAdmin(admin.ModelAdmin):
    """
    Admin configuration for StudentsGroup model.
    """
    list_display = ["teacher", "scheduled_at", "max_students", "created_at"]
    list_filter = ["scheduled_at", "created_at", "updated_at"]
    search_fields = ["teacher__name"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["scheduled_at"]
    list_per_page = 20
    filter_horizontal = ["students"]
    actions = [soft_delete_selected]

    fieldsets = (
        ("Group Information", {
            "fields": ("teacher", "scheduled_at", "max_students")
        }),
        ("Students", {
            "fields": ("students",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin configuration for Lesson model.
    """
    list_display = ["teacher", "students_group", "occurred_at", "created_at"]
    list_filter = ["occurred_at", "created_at", "updated_at"]
    search_fields = ["teacher__name", "notes"]
    readonly_fields = ["created_at", "updated_at", "deleted_at"]
    ordering = ["-occurred_at"]
    list_per_page = 20
    actions = [soft_delete_selected]

    fieldsets = (
        ("Lesson Information", {
            "fields": ("students_group", "teacher", "occurred_at")
        }),
        ("Notes", {
            "fields": ("notes",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "deleted_at"),
            "classes": ("collapse",)
        }),
    )
