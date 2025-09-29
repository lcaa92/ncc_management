"""
Pytest configuration for Django tests.
"""

import os
import django
from django.conf import settings
from django.test.utils import get_runner

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ncc_school_management.test_settings")

# Configure Django
django.setup()

# Configure pytest-django
pytest_plugins = ["pytest_django"]
