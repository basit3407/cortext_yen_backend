from django.shortcuts import get_object_or_404
from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from drf_yasg import openapi
from django.utils.html import format_html, format_html_join
from .filters import BlogFilter, FabricFilter
from .pagination import CustomPagination
from .models import (
    Blog,
    BlogCategory,
    Cart,
    CartItem,
    ContactDetails,
    ContactRequest,
    CustomUser,
    Event,
    Fabric,
    FabricColorCategory,
    Favorite,
    ProductCategory,
    MediaUploads,
    Order,
    OrderItem,
)
from .serializers import (
    BlogCategorySerializer,
    BlogCategoryCreateUpdateSerializer,
    BlogSerializer,
    BlogCreateUpdateSerializer,
    CartItemSerializer,
    ContactDetailsSerializer,
    ContactDetailsCreateUpdateSerializer,
    ContactFormSerializer,
    ContactRequestSerializer,
    ContactRequestCreateUpdateSerializer,
    EventSerializer,
    EventCreateUpdateSerializer,
    FabricColorCategorySerializer,
    FabricColorCategoryCreateUpdateSerializer,
    FabricCreateUpdateSerializer,
    FabricListSerializer,
    FabricSerializer,
    FavoriteSerializer,
    MediaUploadsSerializer,
    OrderItemSerializer,
    OrderSerializer,
    OrderCreateUpdateSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProductCategorySerializer,
    ProductCategoryCreateUpdateSerializer,
    RetreveUpdateUserSerializer,
    SubscriptionSerializer,
    UserLoginSerializer,
    UserSerializer,
    CustomUserCreateUpdateSerializer,
    FabricWithIdsSerializer,
    OrderItemCreateUpdateSerializer,
    ContactRequestWithoutOrderSerializer,
    PublicContactRequestSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.auth.transport import requests
from google.oauth2 import id_token
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
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, filters
from rest_framework.generics import RetrieveUpdateAPIView
from django.core.exceptions import ValidationError
from django.http import Http404
import logging

logger = logging.getLogger(__name__)

"""
# Pagination Information

The following routes use pagination with the CustomPagination class:

1. Product Categories (`/api/product-categories/`)
2. Fabrics (`/api/fabrics/`)
3. Blogs (`/api/blogs/`)
4. Events (`/api/events/`)
5. Orders (`/api/orders/`)
6. Users (`/api/users/`)
7. Contact Details (`/api/contact-details/`)
8. Contact Requests (`/api/contact-requests/`)
9. Public Contact Requests (`/api/contact-requests/public/`)
10. Media Uploads (`/api/media-uploads/`)
11. Admin Orders (`/api/admin/orders/`)

All paginated routes accept the following query parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10)

The response will include:
- `count`: Total number of items
- `next`: URL to the next page (null if no next page)
- `previous`: URL to the previous page (null if no previous page)
- `results`: Array of items for the current page

Example paginated response:
```json
{
    "count": 100,
    "next": "http://api.example.com/items/?page=2",
    "previous": null,
    "results": [
        // items for current page
    ]
}
```

# API Routes Documentation
"""

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

        try:
            decoded_token = id_token.verify_firebase_token(
                id_token_value, requests.Request(), "corlee-85a80"
            )
            email = decoded_token["email"]
            name = decoded_token.get("name", "")

            try:
                user = CustomUser.objects.get(email=email)

            except CustomUser.DoesNotExist:

                user = CustomUser.objects.create_user(email=email, username=email)
                user.name = name
                user.auth_method = "google"
                user.is_verified = True
                user.save()
                # Create a cart for the new user
                Cart.objects.create(user=user)

                # authenticated_user = authenticate(username=user.username, password=None)
                # print("auth user = ", authenticated_user)

                # if authenticated_user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            return Response(
                {"token": token.key, "user": user_data},
                status=status.HTTP_200_OK,
            )
            # else:
            #     print("i am called")
            #     return Response(
            #         {"error": "Authentication failed"},
            #         status=status.HTTP_401_UNAUTHORIZED,
            #     )

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
            # Create a cart for the new user
            Cart.objects.create(user=user)
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
            return Response(
                {"message": "Email successfully verified"}, status=status.HTTP_200_OK
            )

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
    """
    API endpoint to list all product categories with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    serializer_class = ProductCategorySerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(responses={200: ProductCategorySerializer(many=True)})
    def get_queryset(self):
        return ProductCategory.objects.annotate(
            total_orders=Count("fabric__order")
        ).order_by("-total_orders")
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context


fabric_pagination_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "count": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Total number of fabrics"
        ),
        "next": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI,
            description="Link to next page",
        ),
        "previous": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI,
            description="Link to previous page",
        ),
        "results": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT, ref="#/components/schemas/Fabric"
            ),
        ),
    },
)


class FabricListAPIView(generics.ListAPIView):
    """
    API endpoint to list all fabrics with pagination and filtering.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    
    Filter Parameters:
    - keyword: Search keyword
    - sort_by: Sort by "newest" or "oldest"
    - colors: Filter by colors
    - item_code: Filter by item code
    """
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FabricFilter

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
                description='Sort by "newest" or "oldest"',
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
                "item_code",
                openapi.IN_QUERY,
                description="Filter by item code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER,
                default=1,
            ),
        ],
        responses={200: fabric_pagination_schema},
    )
    def get(self, request, *args, **kwargs):
        try:
            print("Starting FabricListAPIView.get()")
            response = super().get(request, *args, **kwargs)
            print(f"FabricListAPIView.get() completed successfully. Response status: {response.status_code}")
            return response
        except Exception as e:
            import traceback
            print(f"ERROR in FabricListAPIView.get(): {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            # Re-raise the exception to maintain the 500 error for debugging
            raise

    def get_serializer_context(self):
        try:
            print("Starting FabricListAPIView.get_serializer_context()")
            context = super().get_serializer_context()
            print(f"FabricListAPIView.get_serializer_context() completed successfully")
            return context
        except Exception as e:
            import traceback
            print(f"ERROR in FabricListAPIView.get_serializer_context(): {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            # Re-raise the exception to maintain the 500 error for debugging
            raise


class FabricDetailAPIView(generics.RetrieveAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer

    @swagger_auto_schema(responses={200: FabricSerializer()})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context


class FabricDetailWithIdsAPIView(generics.RetrieveAPIView):
    """
    Retrieve a fabric with all image IDs included in the response.
    This endpoint is similar to `/fabrics/<id>/` but includes IDs for all images
    (primary, auxiliary, and model).
    """
    queryset = Fabric.objects.all()
    serializer_class = FabricWithIdsSerializer

    @swagger_auto_schema(
        operation_description="Get fabric details with image IDs included",
        responses={200: FabricWithIdsSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context


class FabricCreateAPIView(generics.ListCreateAPIView):
    queryset = Fabric.objects.all()
    filterset_class = FabricFilter
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FabricCreateUpdateSerializer
        return FabricSerializer
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['product_category', 'title', 'description', 'composition', 'weight', 'finish', 'item_code'],
            properties={
                'product_category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Product category ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric title'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric description'),
                'composition': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric composition'),
                'weight': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric weight'),
                'finish': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric finish'),
                'item_code': openapi.Schema(type=openapi.TYPE_STRING, description='Unique item code'),
                'is_hot_selling': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is hot selling flag'),
                'color_images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'color_category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Color category ID'),
                            'primary_image': openapi.Schema(type=openapi.TYPE_INTEGER, description='Primary image ID (MediaUploads)'),
                            'aux_image1': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 1 ID (optional)'),
                            'aux_image2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 2 ID (optional)'),
                            'aux_image3': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 3 ID (optional)'),
                            'model_image': openapi.Schema(type=openapi.TYPE_INTEGER, description='Model image ID (optional)')
                        },
                        required=['color_category', 'primary_image']
                    ),
                    description='List of color images for the fabric'
                )
            },
        ),
        responses={201: FabricSerializer()},
    )
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in FabricCreateAPIView.get: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching fabrics"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in FabricCreateAPIView.post: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in FabricCreateAPIView.post: {str(e)}")
            return Response(
                {"error": "An error occurred while creating the fabric"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        responses={200: fabric_pagination_schema},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FabricUpdateAPIView(generics.UpdateAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricCreateUpdateSerializer
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Product category ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric title'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric description'),
                'composition': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric composition'),
                'weight': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric weight'),
                'finish': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric finish'),
                'item_code': openapi.Schema(type=openapi.TYPE_STRING, description='Unique item code'),
                'is_hot_selling': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is hot selling flag'),
                'color_images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'color_category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Color category ID'),
                            'primary_image': openapi.Schema(type=openapi.TYPE_INTEGER, description='Primary image ID (MediaUploads)'),
                            'aux_image1': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 1 ID (optional)'),
                            'aux_image2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 2 ID (optional)'),
                            'aux_image3': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 3 ID (optional)'),
                            'model_image': openapi.Schema(type=openapi.TYPE_INTEGER, description='Model image ID (optional)')
                        }
                    ),
                    description='List of color images for the fabric'
                )
            },
        ),
        responses={200: FabricSerializer()},
    )
    def put(self, request, *args, **kwargs):
        try:
            return super().put(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in FabricUpdateAPIView.put: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in FabricUpdateAPIView.put: {str(e)}")
            return Response(
                {"error": "An error occurred while updating the fabric"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Product category ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric title'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric description'),
                'composition': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric composition'),
                'weight': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric weight'),
                'finish': openapi.Schema(type=openapi.TYPE_STRING, description='Fabric finish'),
                'item_code': openapi.Schema(type=openapi.TYPE_STRING, description='Unique item code'),
                'is_hot_selling': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is hot selling flag'),
                'color_images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'color_category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Color category ID'),
                            'primary_image': openapi.Schema(type=openapi.TYPE_INTEGER, description='Primary image ID (MediaUploads)'),
                            'aux_image1': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 1 ID (optional)'),
                            'aux_image2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 2 ID (optional)'),
                            'aux_image3': openapi.Schema(type=openapi.TYPE_INTEGER, description='Auxiliary image 3 ID (optional)'),
                            'model_image': openapi.Schema(type=openapi.TYPE_INTEGER, description='Model image ID (optional)')
                        }
                    ),
                    description='List of color images for the fabric'
                )
            },
        ),
        responses={200: FabricSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class FabricDeleteAPIView(generics.DestroyAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer
    
    @swagger_auto_schema(
        responses={
            204: "No Content",
            400: "Bad Request - Fabric is in use"
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in FabricDeleteAPIView.delete: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in FabricDeleteAPIView.delete: {str(e)}")
            return Response(
                {"error": "An error occurred while deleting the fabric"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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

    @swagger_auto_schema(
        manual_parameters=[
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
        ],
        responses={200: FavoriteSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Favorite.objects.filter(user=self.request.user).select_related(
            "fabric"
        )

        sort_by = self.request.GET.get("sort_by", "newest")
        colors = self.request.GET.getlist("colors", [])

        # Apply sorting based on fabric attributes
        if sort_by == "newest":
            queryset = queryset.order_by("-fabric__created_at")
        elif sort_by == "oldest":
            queryset = queryset.order_by("fabric__created_at")

        # Apply color filters based on related FabricColorImage objects
        if colors:
            queryset = queryset.filter(
                fabric__color_images__color__in=colors
            ).distinct()

        return queryset


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


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage events with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    queryset = Event.objects.all()
    pagination_class = CustomPagination
    serializer_class = EventSerializer

    @swagger_auto_schema(responses={200: EventSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context


class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage blogs with pagination and filtering.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    
    Filter Parameters:
    - category: Filter by blog category
    - search: Search in title, content, and category name
    - ordering: Sort by created_at, title, or view_count
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    filterset_class = BlogFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category"]
    search_fields = ["title", "content", "category__name"]
    ordering_fields = [
        "created_at",
        "title",
        "view_count",
    ]
    ordering = ["-created_at"]  # Default ordering
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogCreateUpdateSerializer
        return BlogSerializer

    @swagger_auto_schema(responses={200: BlogSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: BlogSerializer()})
    def retrieve(self, request, *args, **kwargs):
        # Increment view count on retrieve
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BlogCreateUpdateSerializer,
        responses={201: BlogSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BlogCreateUpdateSerializer,
        responses={200: BlogSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BlogCreateUpdateSerializer,
        responses={200: BlogSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: "No Content"})
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            # If the blog doesn't exist, return 404
            return Response(
                {"error": "Blog not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # For other exceptions, return 400
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ContactFormView(APIView):

    @swagger_auto_schema(
        request_body=ContactFormSerializer,
        responses={200: "Contact form submitted successfully", 400: "Invalid input"},
        operation_description="Submit the contact form",
    )
    def post(self, request, *args, **kwargs):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            subject = validated_data["subject"]
            message = validated_data["description"]
            item_code = validated_data.get("item_code", "")
            name = validated_data["name"]
            email = validated_data["email"]
            phone_number = validated_data["phone_number"]
            company_name = validated_data["company_name"]
            request_type = validated_data["request_type"]
            sample_requested = validated_data["sample_requested"]
            request_status = request.data.get("status", "new")  # Changed variable name to request_status

            fabric = None
            if item_code:
                try:
                    fabric = Fabric.objects.get(item_code=item_code)
                except Fabric.DoesNotExist:
                    return Response(
                        {"error": "Fabric with the given item code not found."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Set the appropriate status field based on request_type
            status_data = {}
            if request_type == "product_request":
                status_data["order_status"] = request_status
            else:
                status_data["current_status"] = request_status

            contact_request = ContactRequest.objects.create(
                user=request.user if request.user.is_authenticated else None,
                email=email,  # Always set email from form data
                subject=subject,
                message=message,
                company_name=company_name,
                name=name,
                phone=phone_number,
                sample_requested=sample_requested,
                request_type=request_type,
                related_fabric=fabric if request_type == "product" else None,
                **status_data  # Add the appropriate status field
            )

            # Send email to admin
            email_subject = f"New {subject} from {name}"
            email_message = f"""
            Item Code: {item_code or 'N/A'}
            Name: {name}
            Email: {email}
            Phone Number: {phone_number}
            Company Name: {company_name}
            Sample Requested: {"Yes" if sample_requested else "No"}
            Description: {message}
            Status: {request_status}
            """

            try:
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["corleeandco@gmail.com", "corleeit@gmail.com"],
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to send email. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Send confirmation email to the user
            user_email_subject = "We Have Received Your Request"
            user_email_message = f"""
            Dear {name},

            Thank you for reaching out to us. We have received your request and will get back to you shortly.

            Here are the details of your request:
            Request Number: {contact_request.request_number}
            Subject: {subject}
            Description: {message}
            Item Code: {item_code or 'N/A'}
            Company Name: {company_name}
            Sample Requested: {"Yes" if sample_requested else "No"}
            Status: {request_status}

            If you have any further questions, please don't hesitate to contact us.

            Best regards,
            The Team
            """

            try:
                send_mail(
                    subject=user_email_subject,
                    message=user_email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
            except Exception as e:
                # Log the error if needed
                pass  # You might want to handle this case too

            return Response(
                {
                    "message": "Contact form submitted successfully.",
                    "request_number": contact_request.request_number,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return CartItem.objects.none()

        cart = get_object_or_404(Cart, user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    @swagger_auto_schema(
        responses={200: CartItemSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        user_data = RetreveUpdateUserSerializer(user).data
        cart_items_data = CartItemSerializer(
            cart_items, many=True, context={"request": request}
        ).data

        response_data = {"user": user_data, "cart_items": cart_items_data}

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CartItemSerializer,
        responses={201: CartItemSerializer(), 400: "Invalid input"},
    )
    def create(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        fabric_id = request.data.get("fabric_id")
        color = request.data.get("color")

        existing_item = CartItem.objects.filter(
            cart=cart, fabric_id=fabric_id, color=color
        ).first()

        if existing_item:
            existing_item.quantity += int(request.data.get("quantity", 1))
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={204: "No Content"})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method="post",
    responses={
        201: openapi.Response("Order created", OrderSerializer),
        400: "Invalid input",
    },
    security=[{"token": []}],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    order_data = {
        "user_id": request.user.id,
        "items": [],
    }

    for item in cart_items:
        order_data["items"].append(
            {
                "fabric_id": item.fabric.id,
                "color": item.color,
                "quantity": item.quantity,
            }
        )

    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order = order_serializer.save()

        # Create a ContactRequest for the product request
        contact_request = ContactRequest.objects.create(
            user=request.user,
            request_type="product_request",
            subject="Product request generated from checkout",
            message="Product request generated from checkout",
            company_name=request.user.company_name,
            related_order=order,
        )

        # Generate the HTML table for the email
        table_rows = format_html_join(
            "\n",
            "<tr><td>{}</td><td>{}</td><td>{}</td><td><img src='{}' width='50' height='50'></td><td>{}</td></tr>",
            [
                (
                    idx,
                    order.order_date.strftime("%Y-%m-%d"),  # Order Date
                    item.fabric.item_code,  # Item Code
                    (
                        item.fabric.color_images.first().primary_image.file.url
                        if item.fabric.color_images.exists()
                        else ""
                    ),
                    item.quantity,
                )
                for idx, item in enumerate(cart_items, start=1)
            ],
        )

        table_html = format_html(
            """
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="padding: 8px; text-align: left;">S.No</th>
                        <th style="padding: 8px; text-align: left;">Order Date</th>
                        <th style="padding: 8px; text-align: left;">Item Code</th>
                        <th style="padding: 8px; text-align: left;">Image</th>
                        <th style="padding: 8px; text-align: left;">Quantity</th>
                    </tr>
                </thead>
                <tbody>
                    {}
                </tbody>
            </table>
            """,
            table_rows,
        )

        # Prepare email content
        user_email_subject = "Your Order Summary"
        user_email_message = format_html(
            f"""
            <p>Dear {request.user.name},</p>
            <p>Thank you for placing your order. Your request number to track this order is <strong>{contact_request.request_number}</strong>.</p>
            <p>Below is the summary of your order:</p>
            {table_html}
            <p>We will process your order soon. Thank you for shopping with us!</p>
            """
        )

        admin_email_subject = "New Order Received"
        admin_email_message = format_html(
            f"""
            <p>A new order has been placed by {request.user.username}. Below is the summary of the order:</p>
            {table_html}
            """
        )

        # Send email to user
        user_email = EmailMessage(
            user_email_subject,
            user_email_message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
        )
        user_email.content_subtype = "html"  # To send the email in HTML format
        user_email.send()

        # Send email to admin
        admin_email = EmailMessage(
            admin_email_subject,
            admin_email_message,
            settings.DEFAULT_FROM_EMAIL,
            ["corleeandco@gmail.com"],
        )
        admin_email.content_subtype = "html"
        admin_email.send()

        # Clear the cart
        cart_items.delete()

        return Response(
            {
                "request_number": contact_request.request_number,
                "message": "Order placed successfully.",
            },
            status=status.HTTP_201_CREATED,
        )

    else:
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactRequestListCreateAPIView(
    # generics.ListCreateAPIView
    generics.ListAPIView
):
    serializer_class = ContactRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="List all contact requests for the authenticated user",
        responses={200: ContactRequestSerializer(many=True)},
        security=[{"token": []}],
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER
            ),
        ]
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
        user = self.request.user
        if user.is_staff:
            return ContactRequest.objects.select_related('user', 'related_fabric', 'related_order').all()
        return ContactRequest.objects.select_related('user', 'related_fabric', 'related_order').filter(user=user)


class ContactRequestDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ContactRequestCreateUpdateSerializer
        return ContactRequestSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a specific contact request for the authenticated user",
        responses={200: ContactRequestSerializer()},
        security=[{"token": []}],
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific contact request for the authenticated user",
        request_body=ContactRequestCreateUpdateSerializer,
        responses={200: ContactRequestSerializer()},
        security=[{"token": []}],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ContactRequest.objects.select_related('user', 'related_fabric', 'related_order').all()
        return ContactRequest.objects.select_related('user', 'related_fabric', 'related_order').filter(user=user)


class UserAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetreveUpdateUserSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        request_body=RetreveUpdateUserSerializer,
        responses={
            200: RetreveUpdateUserSerializer,
            400: "Invalid data",
            401: "Unauthorized",
        },
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            200: RetreveUpdateUserSerializer,
            401: "Unauthorized",
        }
    )
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactDetailsView(APIView):
    def get(self, request):
        contact_details = ContactDetails.objects.first()
        if contact_details:
            serializer = ContactDetailsSerializer(contact_details)
            return Response(serializer.data)
        return Response(
            {"detail": "No contact details found."}, status=status.HTTP_404_NOT_FOUND
        )


class SubscriptionView(APIView):
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Email subscribed successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FabricColorCategoryListView(generics.ListAPIView):
    queryset = FabricColorCategory.objects.all()
    serializer_class = FabricColorCategorySerializer


class MediaUploadsCreateAPIView(generics.CreateAPIView):
    serializer_class = MediaUploadsSerializer
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['file'],
            properties={
                'file': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='File to upload (image will be automatically converted to WebP format)'
                ),
            },
        ),
        responses={201: MediaUploadsSerializer()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MediaUploadsListAPIView(generics.ListAPIView):
    """
    API endpoint to list all media uploads with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    queryset = MediaUploads.objects.all()
    serializer_class = MediaUploadsSerializer
    pagination_class = CustomPagination
    
    @swagger_auto_schema(
        responses={200: MediaUploadsSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MediaUploadsDetailAPIView(generics.RetrieveAPIView):
    queryset = MediaUploads.objects.all()
    serializer_class = MediaUploadsSerializer
    
    @swagger_auto_schema(
        responses={200: MediaUploadsSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MediaUploadsDeleteAPIView(generics.DestroyAPIView):
    queryset = MediaUploads.objects.all()
    serializer_class = MediaUploadsSerializer
    
    @swagger_auto_schema(
        responses={204: "No Content"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ProductCategory ViewSet for CRUD operations
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCategoryCreateUpdateSerializer
        return ProductCategorySerializer

    @swagger_auto_schema(responses={200: ProductCategorySerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: ProductCategorySerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ProductCategoryCreateUpdateSerializer,
        responses={201: ProductCategorySerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ProductCategoryCreateUpdateSerializer,
        responses={200: ProductCategorySerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ProductCategoryCreateUpdateSerializer,
        responses={200: ProductCategorySerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: "No Content",
            400: "Bad Request - Category is in use"
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# BlogCategory ViewSet for CRUD operations
class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogCategoryCreateUpdateSerializer
        return BlogCategorySerializer

    @swagger_auto_schema(responses={200: BlogCategorySerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: BlogCategorySerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BlogCategoryCreateUpdateSerializer,
        responses={201: BlogCategorySerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BlogCategoryCreateUpdateSerializer,
        responses={200: BlogCategorySerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BlogCategoryCreateUpdateSerializer,
        responses={200: BlogCategorySerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: "No Content"})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# ColorCategory ViewSet for CRUD operations
class FabricColorCategoryViewSet(viewsets.ModelViewSet):
    queryset = FabricColorCategory.objects.all()
    serializer_class = FabricColorCategorySerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FabricColorCategoryCreateUpdateSerializer
        return FabricColorCategorySerializer

    @swagger_auto_schema(responses={200: FabricColorCategorySerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: FabricColorCategorySerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=FabricColorCategoryCreateUpdateSerializer,
        responses={201: FabricColorCategorySerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=FabricColorCategoryCreateUpdateSerializer,
        responses={200: FabricColorCategorySerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=FabricColorCategoryCreateUpdateSerializer,
        responses={200: FabricColorCategorySerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: "No Content",
            400: "Bad Request - Category is in use"
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# Event ViewSet CRUD operations update
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage events with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    queryset = Event.objects.all()
    pagination_class = CustomPagination
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventCreateUpdateSerializer
        return EventSerializer

    @swagger_auto_schema(responses={200: EventSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: EventSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=EventCreateUpdateSerializer,
        responses={201: EventSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=EventCreateUpdateSerializer,
        responses={200: EventSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=EventCreateUpdateSerializer,
        responses={200: EventSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: "No Content"})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Order ViewSet for CRUD operations
class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage orders with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # Return all orders with optimized queries
        return Order.objects.select_related('user').prefetch_related('items__fabric').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateUpdateSerializer
        return OrderSerializer

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: OrderSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=OrderCreateUpdateSerializer,
        responses={201: OrderSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=OrderCreateUpdateSerializer,
        responses={200: OrderSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=OrderCreateUpdateSerializer,
        responses={200: OrderSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: "No Content"})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Users ViewSet for CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage users with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CustomUserCreateUpdateSerializer
        return UserSerializer

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: UserSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CustomUserCreateUpdateSerializer,
        responses={201: UserSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CustomUserCreateUpdateSerializer,
        responses={200: UserSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CustomUserCreateUpdateSerializer,
        responses={200: UserSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: "No Content",
            400: "Bad Request - User deletion failed"
        },
        operation_description="Delete a user and all their related data (orders, favorites, contact requests, cart, and blogs)"
    )
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete user: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


# ContactDetails ViewSet for CRUD operations
class ContactDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage contact details with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    queryset = ContactDetails.objects.all()
    pagination_class = CustomPagination
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ContactDetailsCreateUpdateSerializer
        return ContactDetailsSerializer

    @swagger_auto_schema(responses={200: ContactDetailsSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: ContactDetailsSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ContactDetailsCreateUpdateSerializer,
        responses={201: ContactDetailsSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ContactDetailsCreateUpdateSerializer,
        responses={200: ContactDetailsSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ContactDetailsCreateUpdateSerializer,
        responses={200: ContactDetailsSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: "No Content"})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# ContactRequest ViewSet for CRUD operations
class ContactRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage contact requests with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ContactRequest.objects.select_related('user', 'related_fabric', 'related_order').all()
        return ContactRequest.objects.select_related('user', 'related_fabric', 'related_order').filter(user=user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ContactRequestCreateUpdateSerializer
        return ContactRequestSerializer

    @swagger_auto_schema(responses={200: ContactRequestSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: ContactRequestSerializer()})
    def retrieve(self, request, *args, **kwargs):
        # Make sure to select_related('user') to optimize the query
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ContactRequestCreateUpdateSerializer,
        responses={201: ContactRequestSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ContactRequestCreateUpdateSerializer,
        responses={200: ContactRequestSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ContactRequestCreateUpdateSerializer,
        responses={200: ContactRequestSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: "No Content"})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AllContactRequestsView(generics.ListAPIView):
    """
    API endpoint to list all contact requests for any authenticated user.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    serializer_class = ContactRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="List all contact requests for any authenticated user",
        responses={200: ContactRequestSerializer(many=True)},
        security=[{"token": []}],
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return ContactRequest.objects.select_related('user', 'related_fabric', 'related_order').all()


class PublicContactRequestsView(APIView):
    """
    View to list all contact requests without any authentication requirements.
    This endpoint is publicly accessible and returns contact requests with basic information.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    """
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    
    @swagger_auto_schema(
        operation_description="Get all contact requests without authentication",
        operation_summary="Get all contact requests without authentication",
        responses={
            200: PublicContactRequestSerializer(many=True),
            500: "Internal Server Error"
        },
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get(self, request):
        try:
            # Get all contact requests with optimized queries
            contact_requests = ContactRequest.objects.select_related('user', 'related_fabric').all()
            
            # Apply pagination
            paginator = CustomPagination()
            page = paginator.paginate_queryset(contact_requests, request)
            
            # Serialize the paginated results
            serializer = PublicContactRequestSerializer(page, many=True)
            
            return paginator.get_paginated_response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error in PublicContactRequestsView: {str(e)}", exc_info=True)
            return Response(
                {"error": "An error occurred while fetching contact requests"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminOrderListAPIView(generics.ListAPIView):
    """
    API view to list all orders for admin dashboard with pagination.
    
    Pagination Parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 10)
    
    Filter Parameters:
    - sort_by: Sort by "newest" or "oldest" (default: "newest")
    """
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Get all orders for admin dashboard",
        responses={
            200: OrderSerializer(many=True),
            400: "Bad Request",
            500: "Internal Server Error"
        },
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "sort_by",
                openapi.IN_QUERY,
                description='Sort by "newest" or "oldest"',
                type=openapi.TYPE_STRING,
                enum=["newest", "oldest"]
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            # Get sort parameter
            sort_by = request.query_params.get('sort_by', 'newest')
            
            # Get queryset
            queryset = self.get_queryset()
            
            # Apply sorting
            if sort_by == 'oldest':
                queryset = queryset.order_by('order_date')
            else:  # default to newest
                queryset = queryset.order_by('-order_date')
            
            # Apply pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error in AdminOrderListAPIView: {str(e)}", exc_info=True)
            return Response(
                {"error": "An error occurred while fetching orders"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnalyticsView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Analytics data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'top_ordered_items': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'fabric_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'fabric_title': openapi.Schema(type=openapi.TYPE_STRING),
                                    'total_orders': openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                        'top_ordered_categories': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'category_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'total_orders': openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                        'total_fabrics': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_blogs': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_orders': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_users': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            )
        }
    )
    def get(self, request):
        # Get top 5 most ordered items
        top_ordered_items = OrderItem.objects.values(
            'fabric__id', 'fabric__title'
        ).annotate(
            total_orders=Count('id')
        ).order_by('-total_orders')[:5]

        # Get top 5 most ordered product categories
        top_ordered_categories = OrderItem.objects.values(
            'fabric__product_category__id', 'fabric__product_category__name'
        ).annotate(
            total_orders=Count('id')
        ).order_by('-total_orders')[:5]

        # Get total counts
        total_fabrics = Fabric.objects.count()
        total_blogs = Blog.objects.count()
        total_orders = Order.objects.count()
        total_users = CustomUser.objects.count()

        return Response({
            'top_ordered_items': list(top_ordered_items),
            'top_ordered_categories': list(top_ordered_categories),
            'total_fabrics': total_fabrics,
            'total_blogs': total_blogs,
            'total_orders': total_orders,
            'total_users': total_users,
        })
