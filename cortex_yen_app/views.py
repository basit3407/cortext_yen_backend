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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Blog, CustomUser, Event, Fabric, Favorite, Order, ProductCategory
from .serializers import (
    BlogSerializer,
    EventSerializer,
    FabricSerializer,
    FavoriteSerializer,
    OrderSerializer,
    ProductCategorySerializer,
    UserSerializer,
    UserLoginSerializer,
)


class GoogleLoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "idToken": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Google ID token"
                ),
            },
        ),
        responses={200: "Success", 400: "Invalid token", 401: "Authentication failed"},
    )
    def post(self, request):
        id_token_value = request.data.get("idToken")

        CLIENT_ID = (
            "81090684417-hhflg4bqed9akoo0seelvuirrc3dffv8.apps.googleusercontent.com"
        )

        try:
            decoded_token = id_token.verify_oauth2_token(
                id_token_value, requests.Request(), CLIENT_ID
            )
            email = decoded_token["email"]

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create_user(email=email, username=email)

            authenticated_user = authenticate(username=user.username, password=None)

            if authenticated_user is not None:
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
    @swagger_auto_schema(
        request_body=UserSerializer, responses={201: "Created", 400: "Invalid data"}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: "Success", 400: "Invalid credentials"},
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "verification_token",
                openapi.IN_PATH,
                description="Verification token",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={302: "Redirect", 400: "Invalid token"},
    )
    def get(self, request, verification_token):
        try:
            user = CustomUser.objects.get(verification_token=verification_token)
            user.verify_email()
            frontend_url = "http://www.test.com/verified"
            return HttpResponseRedirect(redirect_to=frontend_url)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid verification token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    subject_template_name = "registration/password_reset_subject.txt"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("password_reset_complete")


class ProductCategoryListAPIView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer

    @swagger_auto_schema(responses={200: ProductCategorySerializer(many=True)})
    def get_queryset(self):
        return ProductCategory.objects.annotate(
            total_orders=Count("fabric__order")
        ).order_by("-total_orders")


class FabricListAPIView(generics.ListAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer


class FabricDetailAPIView(generics.RetrieveAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer


class ToggleFavoriteView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "fabric_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Fabric ID"
                ),
            },
        ),
        responses={201: "Added to favorites", 204: "Removed from favorites"},
    )
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

    @swagger_auto_schema(responses={200: FavoriteSerializer(many=True)})
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(customer_email=request.user.email)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: OrderSerializer()})
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(customer_email=request.user.email)
        order = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class ToggleHotSellingView(generics.UpdateAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(responses={200: FabricSerializer()})
    def patch(self, request, *args, **kwargs):
        fabric = self.get_object()
        fabric.is_hot_selling = not fabric.is_hot_selling
        fabric.save()
        serializer = self.get_serializer(fabric)
        return Response(serializer.data)


class BestSellingFabricsAPIView(generics.ListAPIView):
    serializer_class = FabricSerializer

    @swagger_auto_schema(responses={200: FabricSerializer(many=True)})
    def get_queryset(self):
        return Fabric.objects.annotate(num_orders=Count("orderitem")).order_by(
            "-num_orders"
        )


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
