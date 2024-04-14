# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http import HttpResponseRedirect
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework import generics
from django.db.models import Count
from django.urls import reverse_lazy

from .models import CustomUser, ProductCategory
from .serializers import ProductCategorySerializer, UserSerializer, UserLoginSerializer


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create new user
            token = Token.objects.create(user=user)  # Generate token for user
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    def get(self, request, verification_token):
        try:
            user = CustomUser.objects.get(verification_token=verification_token)
            user.verify_email()
            # Construct the frontend URL to redirect to
            frontend_url = (
                "http://www.test.com/verified"  # Define the frontend URL to redirect to
            )
            # Return a redirect response
            return HttpResponseRedirect(redirect_to=frontend_url)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid verification token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    subject_template_name = (
        "registration/password_reset_subject.txt"  # Optional: Custom subject template
    )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("password_reset_complete")


class ProductCategoryListAPIView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        queryset = ProductCategory.objects.annotate(
            total_orders=Count("fabric__order")
        ).order_by("-total_orders")
        return queryset
