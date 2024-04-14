# urls.py

from django.urls import path
from .views import EmailVerificationView, UserRegistrationAPIView, UserLoginAPIView

urlpatterns = [
    path("api/register/", UserRegistrationAPIView.as_view(), name="user_registration"),
    path("api/login/", UserLoginAPIView.as_view(), name="user_login"),
    path(
        "api/verify-email/<str:verification_token>/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
]
