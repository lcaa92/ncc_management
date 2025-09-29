"""
Management models for the NCC School Management system.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import BaseModel


class StudentsStatus(models.TextChoices):
    """
    Enum for student status.
    """
    ACTIVE = "active", "Active"
    FORMER = "former", "Former"


class TeacherStatus(models.TextChoices):
    """
    Enum for teacher status.
    """
    ACTIVE = "active", "Active"
    FORMER = "former", "Former"


class Student(BaseModel):
    """
    Student model representing enrolled students.
    """
    name = models.CharField(
        max_length=255,
        help_text="Full name of the student"
    )
    birth_date = models.DateField(
        help_text="Date of birth of the student"
    )
    extra_info = models.TextField(
        blank=True,
        null=True,
        help_text="Additional information about the student"
    )
    status = models.CharField(
        max_length=10,
        choices=StudentsStatus.choices,
        default=StudentsStatus.ACTIVE,
        help_text="Current status of the student"
    )

    class Meta:
        db_table = "management_students"
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    """
    Teacher model representing school teachers.
    """
    name = models.CharField(
        max_length=255,
        help_text="Full name of the teacher"
    )
    pix_key = models.CharField(
        max_length=255,
        help_text="PIX key for payments to the teacher"
    )
    status = models.CharField(
        max_length=10,
        choices=TeacherStatus.choices,
        default=TeacherStatus.ACTIVE,
        help_text="Current status of the teacher"
    )

    class Meta:
        db_table = "management_teachers"
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contract(BaseModel):
    """
    Contract model representing student enrollment in products.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="contracts",
        help_text="Student enrolled in the contract"
    )
    product = models.ForeignKey(
        "comercial.Product",
        on_delete=models.CASCADE,
        related_name="contracts",
        help_text="Product or course the student is enrolled in"
    )

    class Meta:
        db_table = "management_contracts"
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created_at"]
        unique_together = ["student", "product"]

    def __str__(self):
        return f"Contract: {self.student.name} - {self.product.name}"


class StudentsGroup(BaseModel):
    """
    Students group model representing classes with scheduled lessons.
    """
    scheduled_at = models.DateTimeField(
        help_text="Scheduled date and time for the group lessons"
    )
    students = models.ManyToManyField(
        Student,
        related_name="groups",
        help_text="Students enrolled in this group"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="groups",
        help_text="Teacher assigned to this group"
    )
    max_students = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Maximum number of students allowed in this group"
    )

    class Meta:
        db_table = "management_students_groups"
        verbose_name = "Students Group"
        verbose_name_plural = "Students Groups"
        ordering = ["scheduled_at"]

    def __str__(self):
        return f"Group with {self.teacher.name} at {self.scheduled_at}"

    @property
    def current_students_count(self):
        """
        Get the current number of students in the group.
        """
        return self.students.filter(deleted_at__isnull=True).count()


class Lesson(BaseModel):
    """
    Lesson model representing individual class sessions.
    """
    students_group = models.ForeignKey(
        StudentsGroup,
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text="Group this lesson belongs to"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text="Teacher who conducted the lesson"
    )
    occurred_at = models.DateTimeField(
        help_text="Date and time when the lesson took place"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about the lesson content or student performance"
    )

    class Meta:
        db_table = "management_lessons"
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ["-occurred_at"]

    def __str__(self):
        return f"Lesson with {self.teacher.name} at {self.occurred_at}"
