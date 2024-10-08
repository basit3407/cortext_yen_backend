from django.urls import path, include
from rest_framework import routers
from .views import (
    # BestSellingFabricsAPIView,
    BlogCategoryViewSet,
    BlogViewSet,
    CartItemViewSet,
    ContactDetailsView,
    # CartViewSet,
    ContactFormView,
    ContactRequestDetailAPIView,
    ContactRequestListCreateAPIView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    EmailVerificationView,
    EventViewSet,
    FabricColorCategoryListView,
    FabricDetailAPIView,
    FabricListAPIView,
    FavoriteFabricsListView,
    GoogleLoginAPIView,
    # OrderViewSet,
    ProductCategoryListAPIView,
    SubscriptionView,
    ToggleFavoriteView,
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserAPIView,
    checkout,
)

router = routers.DefaultRouter()
# router.register(r"orders", OrderViewSet)
router.register(r"events", EventViewSet)
router.register(r"blogs", BlogViewSet)
router.register(r"blog-categories", BlogCategoryViewSet)

# router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart-items", CartItemViewSet, basename="cartitem")

urlpatterns = [
    path("", include(router.urls)),
    path("contact-details/", ContactDetailsView.as_view(), name="contact-details"),
    path("ckeditor5/", include("django_ckeditor_5.urls")),  # Include CKEditor 5 URLs
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
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_done",
    ),
    # path(
    #     "best_selling_fabrics/",
    #     BestSellingFabricsAPIView.as_view(),
    #     name="best-selling-fabrics",
    # ),
    path("contact/", ContactFormView.as_view(), name="contact_form"),
    path("checkout/", checkout, name="checkout"),
    path(
        "contact-requests/",
        ContactRequestListCreateAPIView.as_view(),
        name="contact-requests",
    ),
    path(
        "contact-requests/<int:pk>/",
        ContactRequestDetailAPIView.as_view(),
        name="contact-request-detail",
    ),
    path("user/", UserAPIView.as_view(), name="user-update"),
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
    path(
        "color-categories/",
        FabricColorCategoryListView.as_view(),
        name="color-category-list",
    ),
]
