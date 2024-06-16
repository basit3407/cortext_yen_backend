from django.urls import path, include
from django.contrib.auth import views as auth_views  # Add this import
from rest_framework import routers
from .views import (
    BestSellingFabricsAPIView,
    BlogViewSet,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    EmailVerificationView,
    EventViewSet,
    FabricDetailAPIView,
    FabricListAPIView,
    FavoriteFabricsListView,
    GoogleLoginAPIView,
    OrderViewSet,
    ProductCategoryListAPIView,
    ToggleFavoriteView,
    UserRegistrationAPIView,
    UserLoginAPIView,
)

router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet)
router.register(r"events", EventViewSet)
router.register(r"blogs", BlogViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationAPIView.as_view(), name="user_registration"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("google-login/", GoogleLoginAPIView.as_view(), name="google_login"),
    path(
        "verify-email/<str:verification_token>/",
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
    path("toggle_favorite/", ToggleFavoriteView.as_view(), name="toggle-favorite"),
    path(
        "favorite_fabrics/",
        FavoriteFabricsListView.as_view(),
        name="favorite-fabrics-list",
    ),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "best_selling_fabrics/",
        BestSellingFabricsAPIView.as_view(),
        name="best-selling-fabrics",
    ),
]
