"""
API serializers for the NCC School Management system.
"""

from rest_framework import serializers
from comercial.models import Product
from financial.models import Payment, TeacherPayments
from management.models import (
    Student, Teacher, Contract, StudentsGroup, Lesson
)
from crm.models import Lead


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    class Meta:
        model = Product
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model.
    """
    payment_method_display = serializers.CharField(
        source="get_payment_method_display",
        read_only=True
    )

    class Meta:
        model = Payment
        fields = "__all__"


class TeacherPaymentsSerializer(serializers.ModelSerializer):
    """
    Serializer for TeacherPayments model.
    """
    teacher_name = serializers.CharField(source="teacher.name", read_only=True)
    payment_method_display = serializers.CharField(
        source="get_payment_method_display",
        read_only=True
    )

    class Meta:
        model = TeacherPayments
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model.
    """
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True
    )

    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for Teacher model.
    """
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True
    )

    class Meta:
        model = Teacher
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    """
    Serializer for Contract model.
    """
    student_name = serializers.CharField(source="student.name", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Contract
        fields = "__all__"


class StudentsGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentsGroup model.
    """
    teacher_name = serializers.CharField(source="teacher.name", read_only=True)
    current_students_count = serializers.ReadOnlyField()
    students_names = serializers.StringRelatedField(
        source="students",
        many=True,
        read_only=True
    )

    class Meta:
        model = StudentsGroup
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for Lesson model.
    """
    teacher_name = serializers.CharField(source="teacher.name", read_only=True)
    group_info = serializers.CharField(
        source="students_group.__str__",
        read_only=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class LeadSerializer(serializers.ModelSerializer):
    """
    Serializer for Lead model.
    """
    class Meta:
        model = Lead
        fields = "__all__"
