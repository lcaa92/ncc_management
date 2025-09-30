"""
Tests for comercial models.
"""

from django.test import TestCase
from decimal import Decimal

from .models import Product


class ProductModelTest(TestCase):
    """
    Test cases for Product model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.product_data = {
            "name": "Python Programming Course",
            "description": "Learn Python from basics to advanced",
            "price": Decimal("299.99"),
            "duration": 6,
            "is_active": True,
        }

    def test_create_product(self):
        """
        Test creating a product.
        """
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.name, "Python Programming Course")
        self.assertEqual(product.price, Decimal("299.99"))
        self.assertEqual(product.duration, 6)
        self.assertTrue(product.is_active)

    def test_product_str_representation(self):
        """
        Test string representation of Product.
        """
        product = Product.objects.create(**self.product_data)
        self.assertEqual(str(product), "Python Programming Course")

    def test_product_meta_options(self):
        """
        Test Product model meta options.
        """
        self.assertEqual(Product._meta.db_table, "comercial_products")
        self.assertEqual(Product._meta.verbose_name, "Product")
        self.assertEqual(Product._meta.verbose_name_plural, "Products")

    def test_product_ordering(self):
        """
        Test Product model ordering.
        """
        Product.objects.create(name="Z Course", price=Decimal("100"), duration=1)
        Product.objects.create(name="A Course", price=Decimal("200"), duration=2)

        products = Product.objects.all()
        self.assertEqual(products[0].name, "A Course")
        self.assertEqual(products[1].name, "Z Course")

    def test_product_soft_delete(self):
        """
        Test Product soft delete functionality.
        """
        product = Product.objects.create(**self.product_data)
        product_id = product.id

        product.delete()

        # Should still exist in database but with deleted_at set
        self.assertIsNotNone(Product.objects.all_with_deleted().get(id=product_id).deleted_at)

        # Should not appear in default queryset
        self.assertFalse(Product.objects.filter(id=product_id).exists())

    def test_product_timestamps(self):
        """
        Test Product timestamp fields.
        """
        product = Product.objects.create(**self.product_data)
        self.assertIsNotNone(product.created_at)
        self.assertIsNotNone(product.updated_at)
