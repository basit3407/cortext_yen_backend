# views.py

from django.shortcuts import get_object_or_404
from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from django.contrib.auth import authenticate
from google.auth.transport import requests
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http import HttpResponseRedirect
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.db.models import Count
from django.urls import reverse_lazy
from .models import CustomUser, Fabric, Favorite, Order, ProductCategory
from .serializers import (
    FabricSerializer,
    FavoriteSerializer,
    OrderSerializer,
    ProductCategorySerializer,
    UserSerializer,
    UserLoginSerializer,
)


class GoogleLoginAPIView(APIView):
    def post(self, request):
        id_token_value = request.data.get("idToken")  # Get ID token from frontend

        # Specify your Google OAuth2 Client ID
        CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"

        try:
            # Verify and decode the ID token using the Google OAuth2 Client ID
            decoded_token = id_token.verify_oauth2_token(
                id_token_value, requests.Request(), CLIENT_ID
            )

            # Extract user information from decoded token
            email = decoded_token["email"]

            # Check if user with this email exists in the database
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # Create a new user if the email doesn't exist
                user = CustomUser.objects.create_user(
                    email=email, username=email
                )  # Use email as username

            # Authenticate the user (check if user exists and return the user object)
            authenticated_user = authenticate(username=user.username, password=None)

            if authenticated_user is not None:
                # Generate token for the authenticated user
                token, _ = Token.objects.get_or_create(user=authenticated_user)

                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Authentication failed"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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


class FabricListAPIView(generics.ListAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer


class FabricDetailAPIView(generics.RetrieveAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer


class ToggleFavoriteView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def post(self, request):
        fabric_id = request.data.get("fabric_id")
        fabric = Fabric.objects.get(pk=fabric_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user, fabric=fabric
        )
        if not created:
            favorite.delete()
            return Response(
                {"detail": "Fabric removed from favorites"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"detail": "Fabric added to favorites"}, status=status.HTTP_201_CREATED
        )


class FavoriteFabricsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [
                permissions.IsAuthenticated()
            ]  # Require authentication for listing and retrieving orders
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(customer_email=request.user.email)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(customer_email=request.user.email)
        order = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class ToggleHotSellingView(generics.UpdateAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer
    permission_classes = [permissions.IsAdminUser]  # Require admin authentication

    def patch(self, request, *args, **kwargs):
        fabric = self.get_object()
        fabric.is_hot_selling = not fabric.is_hot_selling
        fabric.save()
        serializer = self.get_serializer(fabric)
        return Response(serializer.data)


class BestSellingFabricsAPIView(generics.ListAPIView):
    serializer_class = FabricSerializer

    def get_queryset(self):
        # Get fabrics ordered by the number of associated orders (descending)
        return Fabric.objects.annotate(num_orders=Count("orderitem")).order_by(
            "-num_orders"
        )
