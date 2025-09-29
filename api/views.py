"""
API views for the NCC School Management system.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

from .serializers import (
    ProductSerializer, PaymentSerializer, TeacherPaymentsSerializer,
    StudentSerializer, TeacherSerializer, ContractSerializer,
    StudentsGroupSerializer, LessonSerializer, LeadSerializer
)
from comercial.models import Product
from financial.models import Payment, TeacherPayments
from management.models import Student, Teacher, Contract, StudentsGroup, Lesson
from crm.models import Lead


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model.
    """
    queryset = Product.objects.filter(deleted_at__isnull=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "created_at"]
    ordering = ["name"]


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment model.
    """
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["payment_method"]
    search_fields = ["description"]
    ordering_fields = ["value", "paid_at", "created_at"]
    ordering = ["-paid_at"]


class TeacherPaymentsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TeacherPayments model.
    """
    queryset = TeacherPayments.objects.filter(deleted_at__isnull=True)
    serializer_class = TeacherPaymentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["teacher", "payment_method"]
    search_fields = ["description", "teacher__name"]
    ordering_fields = ["value", "paid_at", "created_at"]
    ordering = ["-paid_at"]


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student model.
    """
    queryset = Student.objects.filter(deleted_at__isnull=True)
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["name"]
    ordering_fields = ["name", "birth_date", "created_at"]
    ordering = ["name"]


class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Teacher model.
    """
    queryset = Teacher.objects.filter(deleted_at__isnull=True)
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class ContractViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Contract model.
    """
    queryset = Contract.objects.filter(deleted_at__isnull=True)
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["student", "product"]
    search_fields = ["student__name", "product__name"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class StudentsGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StudentsGroup model.
    """
    queryset = StudentsGroup.objects.filter(deleted_at__isnull=True)
    serializer_class = StudentsGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["teacher"]
    search_fields = ["teacher__name"]
    ordering_fields = ["scheduled_at", "created_at"]
    ordering = ["scheduled_at"]


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lesson model.
    """
    queryset = Lesson.objects.filter(deleted_at__isnull=True)
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["teacher", "students_group"]
    search_fields = ["teacher__name", "notes"]
    ordering_fields = ["occurred_at", "created_at"]
    ordering = ["-occurred_at"]


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lead model.
    """
    queryset = Lead.objects.filter(deleted_at__isnull=True)
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "goals", "interests", "email"]
    ordering_fields = ["name", "birth_date", "created_at"]
    ordering = ["-created_at"]


class CustomTokenObtainPairView(APIView):
    """
    Custom token obtain view that returns access_token, refresh_token, and expires_at.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials or user not active'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Invalid credentials or user not active'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Calculate expiration time
        expires_at = timezone.now() + timedelta(minutes=60)  # Default 60 minutes

        return Response({
            'access_token': str(access_token),
            'refresh_token': str(refresh),
            'expires_at': expires_at.isoformat(),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)
