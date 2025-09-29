"""
API URLs for the NCC School Management system.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    ProductViewSet, PaymentViewSet, TeacherPaymentsViewSet,
    StudentViewSet, TeacherViewSet, ContractViewSet,
    StudentsGroupViewSet, LessonViewSet, LeadViewSet,
    CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"payments", PaymentViewSet)
router.register(r"teacher-payments", TeacherPaymentsViewSet)
router.register(r"students", StudentViewSet)
router.register(r"teachers", TeacherViewSet)
router.register(r"contracts", ContractViewSet)
router.register(r"students-groups", StudentsGroupViewSet)
router.register(r"lessons", LessonViewSet)
router.register(r"leads", LeadViewSet)

urlpatterns = [
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
