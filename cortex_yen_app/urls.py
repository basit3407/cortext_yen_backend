from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import (
    AnalyticsView,
    BlogCategoryViewSet,
    BlogViewSet,
    CartItemViewSet,
    ContactDetailsView,
    ContactDetailsViewSet,
    ContactFormView,
    ContactRequestDetailAPIView,
    ContactRequestListCreateAPIView,
    ContactRequestViewSet,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    EmailVerificationView,
    EventViewSet,
    FabricColorCategoryListView,
    FabricColorCategoryViewSet,
    FabricCreateAPIView,
    FabricDeleteAPIView,
    FabricDetailAPIView,
    FabricDetailWithIdsAPIView,
    FabricListAPIView,
    FabricUpdateAPIView,
    FavoriteFabricsListView,
    GoogleLoginAPIView,
    MediaUploadsCreateAPIView,
    MediaUploadsDeleteAPIView,
    MediaUploadsDetailAPIView,
    MediaUploadsListAPIView,
    OrderViewSet,
    ProductCategoryListAPIView,
    ProductCategoryViewSet,
    SubscriptionView,
    ToggleFavoriteView,
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserAPIView,
    UserViewSet,
    checkout,
    AllContactRequestsView,
    PublicContactRequestsView,
)

router = routers.DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"blogs", BlogViewSet)
router.register(r"blog-categories", BlogCategoryViewSet)
router.register(r"cart-items", CartItemViewSet, basename="cartitem")
router.register(r"product-categories", ProductCategoryViewSet)
router.register(r"color-categories", FabricColorCategoryViewSet)
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"users", UserViewSet, basename="user")
router.register(r"contact-details", ContactDetailsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
    path("contact-details/", ContactDetailsView.as_view(), name="contact-details"),
    path("ckeditor5/", include("django_ckeditor_5.urls")),  # Include CKEditor 5 URLs
    path("register/", UserRegistrationAPIView.as_view(), name="user_registration"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("google-login/", GoogleLoginAPIView.as_view(), name="google_login"),
    path("contact-requests/public/", PublicContactRequestsView.as_view(), name="public-contact-requests"),
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
    path("fabrics/", FabricCreateAPIView.as_view(), name="fabric-create-list"),
    path("fabrics/<int:pk>/", FabricDetailAPIView.as_view(), name="fabric-detail"),
    path("fabrics/withids/<int:pk>/", FabricDetailWithIdsAPIView.as_view(), name="fabric-detail-with-ids"),
    path("fabrics/create/", FabricCreateAPIView.as_view(), name="fabric-create"),
    path("fabrics/<int:pk>/update/", FabricUpdateAPIView.as_view(), name="fabric-update"),
    path("fabrics/<int:pk>/delete/", FabricDeleteAPIView.as_view(), name="fabric-delete"),
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
    path("contact/", ContactFormView.as_view(), name="contact_form"),
    path("checkout/", checkout, name="checkout"),
    path("contact-requests/", ContactRequestListCreateAPIView.as_view(), name="contact-requests"),
    path("contact-requests/all/", AllContactRequestsView.as_view(), name="all-contact-requests"),
    path("contact-requests/viewset/", ContactRequestViewSet.as_view({'get': 'list'}), name="contact-requests-viewset"),
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
    path(
        "color-categories/",
        FabricColorCategoryListView.as_view(),
        name="color-category-list",
    ),
    path("media/", MediaUploadsListAPIView.as_view(), name="media-list"),
    path("media/create/", MediaUploadsCreateAPIView.as_view(), name="media-create"),
    path("media/<int:pk>/", MediaUploadsDetailAPIView.as_view(), name="media-detail"),
    path("media/<int:pk>/delete/", MediaUploadsDeleteAPIView.as_view(), name="media-delete"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
