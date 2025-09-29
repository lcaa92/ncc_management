"""
Tests for management models.
"""

import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

from .models import (
    Student, Teacher, Contract, StudentsGroup, Lesson,
    StudentsStatus, TeacherStatus
)
from comercial.models import Product


class StudentModelTest(TestCase):
    """
    Test cases for Student model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.student_data = {
            "name": "John Doe",
            "birth_date": date(2000, 1, 1),
            "extra_info": "Likes programming",
            "status": StudentsStatus.ACTIVE,
        }

    def test_create_student(self):
        """
        Test creating a student.
        """
        student = Student.objects.create(**self.student_data)
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(student.birth_date, date(2000, 1, 1))
        self.assertEqual(student.status, StudentsStatus.ACTIVE)

    def test_student_str_representation(self):
        """
        Test string representation of Student.
        """
        student = Student.objects.create(**self.student_data)
        self.assertEqual(str(student), "John Doe")

    def test_student_status_choices(self):
        """
        Test StudentsStatus enum choices.
        """
        self.assertEqual(StudentsStatus.ACTIVE, "active")
        self.assertEqual(StudentsStatus.FORMER, "former")


class TeacherModelTest(TestCase):
    """
    Test cases for Teacher model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.teacher_data = {
            "name": "Jane Smith",
            "pix_key": "jane@example.com",
            "status": TeacherStatus.ACTIVE,
        }

    def test_create_teacher(self):
        """
        Test creating a teacher.
        """
        teacher = Teacher.objects.create(**self.teacher_data)
        self.assertEqual(teacher.name, "Jane Smith")
        self.assertEqual(teacher.pix_key, "jane@example.com")
        self.assertEqual(teacher.status, TeacherStatus.ACTIVE)

    def test_teacher_str_representation(self):
        """
        Test string representation of Teacher.
        """
        teacher = Teacher.objects.create(**self.teacher_data)
        self.assertEqual(str(teacher), "Jane Smith")

    def test_teacher_status_choices(self):
        """
        Test TeacherStatus enum choices.
        """
        self.assertEqual(TeacherStatus.ACTIVE, "active")
        self.assertEqual(TeacherStatus.FORMER, "former")


class ContractModelTest(TestCase):
    """
    Test cases for Contract model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.student = Student.objects.create(
            name="John Doe",
            birth_date=date(2000, 1, 1)
        )
        self.product = Product.objects.create(
            name="Python Course",
            price=299.99,
            duration_months=6
        )

    def test_create_contract(self):
        """
        Test creating a contract.
        """
        contract = Contract.objects.create(
            student=self.student,
            product=self.product
        )
        self.assertEqual(contract.student, self.student)
        self.assertEqual(contract.product, self.product)

    def test_contract_str_representation(self):
        """
        Test string representation of Contract.
        """
        contract = Contract.objects.create(
            student=self.student,
            product=self.product
        )
        expected_str = f"Contract: {self.student.name} - {self.product.name}"
        self.assertEqual(str(contract), expected_str)

    def test_contract_unique_together(self):
        """
        Test Contract unique_together constraint.
        """
        Contract.objects.create(student=self.student, product=self.product)

        # Should raise IntegrityError when trying to create duplicate
        with self.assertRaises(Exception):
            Contract.objects.create(student=self.student, product=self.product)


class StudentsGroupModelTest(TestCase):
    """
    Test cases for StudentsGroup model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.teacher = Teacher.objects.create(
            name="Jane Smith",
            pix_key="jane@example.com"
        )
        self.student1 = Student.objects.create(
            name="John Doe",
            birth_date=date(2000, 1, 1)
        )
        self.student2 = Student.objects.create(
            name="Alice Smith",
            birth_date=date(2001, 2, 2)
        )

    def test_create_students_group(self):
        """
        Test creating a students group.
        """
        group = StudentsGroup.objects.create(
            scheduled_at=timezone.now(),
            teacher=self.teacher,
            max_students=10
        )
        group.students.add(self.student1, self.student2)

        self.assertEqual(group.teacher, self.teacher)
        self.assertEqual(group.max_students, 10)
        self.assertEqual(group.students.count(), 2)

    def test_students_group_str_representation(self):
        """
        Test string representation of StudentsGroup.
        """
        group = StudentsGroup.objects.create(
            scheduled_at=timezone.now(),
            teacher=self.teacher
        )
        expected_str = f"Group with {self.teacher.name} at {group.scheduled_at}"
        self.assertEqual(str(group), expected_str)

    def test_current_students_count_property(self):
        """
        Test current_students_count property.
        """
        group = StudentsGroup.objects.create(
            scheduled_at=timezone.now(),
            teacher=self.teacher
        )
        group.students.add(self.student1, self.student2)

        self.assertEqual(group.current_students_count, 2)


class LessonModelTest(TestCase):
    """
    Test cases for Lesson model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.teacher = Teacher.objects.create(
            name="Jane Smith",
            pix_key="jane@example.com"
        )
        self.group = StudentsGroup.objects.create(
            scheduled_at=timezone.now(),
            teacher=self.teacher
        )

    def test_create_lesson(self):
        """
        Test creating a lesson.
        """
        lesson = Lesson.objects.create(
            students_group=self.group,
            teacher=self.teacher,
            occurred_at=timezone.now(),
            notes="Great lesson!"
        )
        self.assertEqual(lesson.students_group, self.group)
        self.assertEqual(lesson.teacher, self.teacher)
        self.assertEqual(lesson.notes, "Great lesson!")

    def test_lesson_str_representation(self):
        """
        Test string representation of Lesson.
        """
        lesson = Lesson.objects.create(
            students_group=self.group,
            teacher=self.teacher,
            occurred_at=timezone.now()
        )
        expected_str = f"Lesson with {self.teacher.name} at {lesson.occurred_at}"
        self.assertEqual(str(lesson), expected_str)
