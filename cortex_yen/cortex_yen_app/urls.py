# urls.py

from django.urls import path
from .views import (
    EmailVerificationView,
    FabricDetailAPIView,
    FabricListAPIView,
    OrderCreateAPIView,
    ProductCategoryListAPIView,
    UserRegistrationAPIView,
    UserLoginAPIView,
)

urlpatterns = [
    path("api/register/", UserRegistrationAPIView.as_view(), name="user_registration"),
    path("api/login/", UserLoginAPIView.as_view(), name="user_login"),
    path(
        "api/verify-email/<str:verification_token>/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
    path(
        "categories/",
        ProductCategoryListAPIView.as_view(),
        name="product-category-list",
    ),
    path("fabrics/", FabricListAPIView.as_view(), name="fabric-list"),
    path("fabrics/<int:pk>/", FabricDetailAPIView.as_view(), name="fabric-detail"),
    path("orders/create/", OrderCreateAPIView.as_view(), name="order-create"),
]
