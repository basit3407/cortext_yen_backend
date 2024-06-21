from django.shortcuts import get_object_or_404
from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from drf_yasg import openapi
from .models import Blog, CustomUser, Event, Fabric, Favorite, Order, ProductCategory
from .serializers import (
    BlogSerializer,
    ContactFormSerializer,
    EventSerializer,
    FabricSerializer,
    FavoriteSerializer,
    OrderSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProductCategorySerializer,
    UserSerializer,
    UserLoginSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.auth.transport import requests
from google.oauth2 import id_token
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.admin import sensitive_post_parameters_m
from rest_framework.generics import GenericAPIView


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
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "token": openapi.Schema(type=openapi.TYPE_STRING),
                        "user": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "username": openapi.Schema(type=openapi.TYPE_STRING),
                                "email": openapi.Schema(type=openapi.TYPE_STRING),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "company_name": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                "address": openapi.Schema(type=openapi.TYPE_STRING),
                                "phone": openapi.Schema(type=openapi.TYPE_STRING),
                                "mobile_phone": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                "is_verified": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN
                                ),
                                "auth_method": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            400: "Invalid token",
            401: "Authentication failed",
        },
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
                user.auth_method = "google"
                user.is_verified = True
                user.save()

            authenticated_user = authenticate(username=user.username, password=None)

            if authenticated_user is not None:
                token, _ = Token.objects.get_or_create(user=authenticated_user)
                user_data = UserSerializer(user).data
                return Response(
                    {"token": token.key, "user": user_data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Authentication failed"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: openapi.Response(
                description="Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "token": openapi.Schema(type=openapi.TYPE_STRING),
                        "user": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "username": openapi.Schema(type=openapi.TYPE_STRING),
                                "email": openapi.Schema(type=openapi.TYPE_STRING),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "company_name": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                "address": openapi.Schema(type=openapi.TYPE_STRING),
                                "phone": openapi.Schema(type=openapi.TYPE_STRING),
                                "mobile_phone": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                "is_verified": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN
                                ),
                                "auth_method": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            400: "Invalid data",
        },
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            user_data = UserSerializer(user).data
            return Response(
                {"token": token.key, "user": user_data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "token": openapi.Schema(type=openapi.TYPE_STRING),
                        "user": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "username": openapi.Schema(type=openapi.TYPE_STRING),
                                "email": openapi.Schema(type=openapi.TYPE_STRING),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "company_name": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                "address": openapi.Schema(type=openapi.TYPE_STRING),
                                "phone": openapi.Schema(type=openapi.TYPE_STRING),
                                "mobile_phone": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                "is_verified": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN
                                ),
                                "auth_method": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            400: "Invalid credentials",
        },
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            return Response(
                {"token": token.key, "user": user_data},
                status=status.HTTP_200_OK,
            )
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
            frontend_url = "{settings.FRONTEND_URL}/verified"
            return HttpResponseRedirect(redirect_to=frontend_url)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid verification token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomPasswordResetView(APIView):
    @swagger_auto_schema(
        request_body=PasswordResetRequestSerializer,
        responses={
            200: openapi.Response(description="Password reset email sent"),
            400: openapi.Response(description="Invalid data or user does not exist"),
            429: openapi.Response(description="Too many requests"),
        },
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]

        user = CustomUser.objects.filter(email=email).first()

        if not user:
            # User with the provided email doesn't exist
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.auth_method == "google":
            return Response(
                {
                    "error": "You signed in using Google. Please use Google account recovery."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        reset_url = (
            f"{settings.FRONTEND_URL}/newPass/{urlsafe_base64_encode(force_bytes(user.pk))}/"
            f"{token_generator.make_token(user)}/"
        )
        name = user.first_name

        subject = "Your password reset request"
        button_text = "Reset Your Password"

        # Render HTML content with a button
        html_content = render_to_string(
            "reset_password_email_template.html",
            {
                "name": name,
                "reset_url": reset_url,
                "button_text": button_text,
            },
        )

        from_email = settings.DEFAULT_FROM_EMAIL

        recipient_list = [email]

        try:
            email = EmailMessage(subject, html_content, from_email, recipient_list)
            email.content_subtype = "html"  # Set content type to HTML
            email.send()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error sending email: {e}")
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)


class CustomPasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, uid,
    new_password1, new_password2
    Returns the success/fail message.
    """

    permission_classes = []
    serializer_class = PasswordResetConfirmSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(CustomPasswordResetConfirmView, self).dispatch(*args, **kwargs)

    @swagger_auto_schema(
        request_body=PasswordResetConfirmSerializer,
        responses={
            200: openapi.Response(description="Password updated successfully"),
            400: openapi.Response(description="Invalid data"),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200, data={"message": "Password updated successfully"})


class ProductCategoryListAPIView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer

    @swagger_auto_schema(responses={200: ProductCategorySerializer(many=True)})
    def get_queryset(self):
        return ProductCategory.objects.annotate(
            total_orders=Count("fabric__order")
        ).order_by("-total_orders")


class FabricListAPIView(generics.ListAPIView):
    serializer_class = FabricSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "keyword",
                openapi.IN_QUERY,
                description="Search keyword",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "sort_by",
                openapi.IN_QUERY,
                description="Sort by 'newest' or 'oldest'",
                type=openapi.TYPE_STRING,
                enum=["newest", "oldest"],
            ),
            openapi.Parameter(
                "colors",
                openapi.IN_QUERY,
                description="Filter by colors",
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER,
                default=1,
            ),
        ],
        responses={200: FabricSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Fabric.objects.all()
        keyword = self.request.GET.get("keyword", "").lower()
        sort_by = self.request.GET.get("sort_by", "newest")
        colors = self.request.GET.getlist("colors", [])

        # Apply filters based on keyword
        if keyword:
            if "best selling" in keyword:
                queryset = Fabric.objects.annotate(
                    num_orders=Count("orderitem")
                ).order_by("-num_orders")
            elif "hot selling" in keyword:
                queryset = queryset.filter(is_hot_selling=True)
            else:
                category = ProductCategory.objects.filter(
                    name__icontains=keyword
                ).first()
                if category:
                    queryset = queryset.filter(product_category=category)
                else:
                    queryset = queryset.filter(title__icontains=keyword)

        # Apply sorting
        if sort_by == "newest":
            queryset = queryset.order_by("-created_at")
        elif sort_by == "oldest":
            queryset = queryset.order_by("created_at")

        # Apply color filters
        if colors:
            queryset = queryset.filter(available_colors__overlap=colors)

        return queryset


class FabricDetailAPIView(generics.RetrieveAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer

    @swagger_auto_schema(responses={200: FabricSerializer()})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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
        security=[{"token": []}],
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

    @swagger_auto_schema(
        responses={200: FavoriteSerializer(many=True)}, security=[{"token": []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    @swagger_auto_schema(
        responses={200: OrderSerializer(many=True)}, security=[{"token": []}]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(customer_email=request.user.email)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: OrderSerializer()}, security=[{"token": []}])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(customer_email=request.user.email)
        order = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={201: OrderSerializer()},
        security=[{"token": []}],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer_email=request.user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
        security=[{"token": []}],
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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


# class BestSellingFabricsAPIView(generics.ListAPIView):
#     serializer_class = FabricSerializer

#     @swagger_auto_schema(responses={200: FabricSerializer(many=True)})
#     def get_queryset(self):
#         return Fabric.objects.annotate(num_orders=Count("orderitem")).order_by(
#             "-num_orders"
#         )


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @swagger_auto_schema(responses={200: EventSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    @swagger_auto_schema(responses={200: BlogSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: BlogSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ContactFormView(APIView):

    @swagger_auto_schema(
        request_body=ContactFormSerializer,
        responses={200: "Contact form submitted successfully", 400: "Invalid input"},
        operation_description="Submit the contact form",
    )
    def post(self, request, *args, **kwargs):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            # Send email
            subject = serializer.validated_data["subject"]
            message = f"""
            Item Code: {serializer.validated_data['item_code']}
            Name: {serializer.validated_data['name']}
            Email: {serializer.validated_data['email']}
            Phone Number: {serializer.validated_data['phone_number']}
            Company Name: {serializer.validated_data.get('company_name', '')}
            Description: {serializer.validated_data.get('description', '')}
            """
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["support@corleeandco.com"],
            )
            return Response(
                {"message": "Contact form submitted successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
