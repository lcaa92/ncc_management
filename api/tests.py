"""
Tests for API views and serializers.
"""

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from datetime import datetime, date

from comercial.models import Product
from financial.models import Payment, TeacherPayments, PaymentMethod
from management.models import Student, Teacher, Contract, StudentsGroup, Lesson
from crm.models import Lead


class APITestCase(APITestCase):
    """
    Base API test case with authentication setup.
    """

    def setUp(self):
        """
        Set up test data and authentication.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client = APIClient()

        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")


class ProductAPITest(APITestCase):
    """
    Test cases for Product API endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        super().setUp()
        self.product_data = {
            "name": "Python Course",
            "description": "Learn Python programming",
            "price": "299.99",
            "duration_months": 6,
            "is_active": True,
        }

    def test_create_product(self):
        """
        Test creating a product via API.
        """
        url = reverse("product-list")
        response = self.client.post(url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_list_products(self):
        """
        Test listing products via API.
        """
        Product.objects.create(**{
            "name": "Python Course",
            "price": Decimal("299.99"),
            "duration_months": 6
        })

        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_product(self):
        """
        Test retrieving a specific product via API.
        """
        product = Product.objects.create(**{
            "name": "Python Course",
            "price": Decimal("299.99"),
            "duration_months": 6
        })

        url = reverse("product-detail", kwargs={"pk": product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Python Course")

    def test_update_product(self):
        """
        Test updating a product via API.
        """
        product = Product.objects.create(**{
            "name": "Python Course",
            "price": Decimal("299.99"),
            "duration_months": 6
        })

        url = reverse("product-detail", kwargs={"pk": product.pk})
        update_data = {"name": "Advanced Python Course"}
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Advanced Python Course")

    def test_delete_product(self):
        """
        Test deleting a product via API.
        """
        product = Product.objects.create(**{
            "name": "Python Course",
            "price": Decimal("299.99"),
            "duration_months": 6
        })

        url = reverse("product-detail", kwargs={"pk": product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Product.objects.all_with_deleted().get(id=product.id).is_deleted)


class StudentAPITest(APITestCase):
    """
    Test cases for Student API endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        super().setUp()
        self.student_data = {
            "name": "John Doe",
            "birth_date": "2000-01-01",
            "extra_info": "Likes programming",
            "status": "active",
        }

    def test_create_student(self):
        """
        Test creating a student via API.
        """
        url = reverse("student-list")
        response = self.client.post(url, self.student_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)

    def test_list_students(self):
        """
        Test listing students via API.
        """
        Student.objects.create(
            name="John Doe",
            birth_date=date(2000, 1, 1)
        )

        url = reverse("student-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class TeacherAPITest(APITestCase):
    """
    Test cases for Teacher API endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        super().setUp()
        self.teacher_data = {
            "name": "Jane Smith",
            "pix_key": "jane@example.com",
            "status": "active",
        }

    def test_create_teacher(self):
        """
        Test creating a teacher via API.
        """
        url = reverse("teacher-list")
        response = self.client.post(url, self.teacher_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 1)

    def test_list_teachers(self):
        """
        Test listing teachers via API.
        """
        Teacher.objects.create(
            name="Jane Smith",
            pix_key="jane@example.com"
        )

        url = reverse("teacher-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class LeadAPITest(APITestCase):
    """
    Test cases for Lead API endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        super().setUp()
        self.lead_data = {
            "name": "John Doe",
            "goals": "Learn Python programming",
            "birth_date": "2000-01-01",
            "interests": "Web development",
            "email": "john@example.com",
            "phone": "+1234567890",
        }

    def test_create_lead(self):
        """
        Test creating a lead via API.
        """
        url = reverse("lead-list")
        response = self.client.post(url, self.lead_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 1)

    def test_list_leads(self):
        """
        Test listing leads via API.
        """
        Lead.objects.create(
            name="John Doe",
            goals="Learn programming",
            birth_date=date(2000, 1, 1)
        )

        url = reverse("lead-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class AuthenticationTest(APITestCase):
    """
    Test cases for API authentication.
    """

    def test_unauthenticated_access(self):
        """
        Test that unauthenticated requests are rejected.
        """
        self.client.credentials()  # Remove authentication

        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_obtain_pair(self):
        """
        Test JWT token obtain endpoint.
        """
        url = reverse("token_obtain_pair")
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("expires_at", response.data)
