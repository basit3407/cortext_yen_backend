from django.db import IntegrityError
from rest_framework import serializers
from .models import (
    Blog,
    # Cart,
    CartItem,
    ContactRequest,
    CustomUser,
    Event,
    Fabric,
    Favorite,
    MediaUploads,
    Order,
    OrderItem,
    ProductCategory,
)
from django.core.mail import send_mail
from django.conf import settings
import logging
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm

logger = logging.getLogger(__name__)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaUploads
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )  # Make password field write-only

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "email",
            "name",
            "company_name",
            "address",
            "phone",
            "mobile_phone",
            "is_verified",
            "auth_method",
        ]

    def create(self, validated_data):
        # Extract and remove the password from validated_data
        password = validated_data.pop("password", None)

        # Create a new CustomUser instance
        try:
            user = CustomUser.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"email": "A user with that email already exists."}
            )

        # Set the password for the user
        if password is not None:
            user.set_password(password)
            user.save()

        # Generate and send verification email
        self.send_verification_email(user)

        return user

    def validate(self, data):
        if data.get("auth_method") == "email" and not data.get("company_name"):
            raise serializers.ValidationError("Company name is required")
        return data

    def send_verification_email(self, user):
        verification_token = user.generate_verification_token()
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        subject = "Verify your email address"
        message = f"Hi {user.name},\n\nPlease click on the following link to verify your email address:\n\n{settings.FRONTEND_URL}/verify-email/{verification_token}/\n\nThanks!"

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logger.error(f"Failed to send email, error: {str(e)}")
            raise


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg)

        attrs["user"] = user
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["name", "company_name", "address", "phone", "mobile_phone", "email"]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "description"]


class ContactFormSerializer(serializers.Serializer):
    item_code = serializers.CharField(max_length=100, required=False, allow_blank=True)
    name = serializers.CharField(max_length=100)
    request_type = serializers.ChoiceField(choices=ContactRequest.REQUEST_TYPE_CHOICES)
    subject = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    company_name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    sample_requested = serializers.BooleanField(default=False)

    def validate(self, data):
        subject = data.get("subject")
        item_code = data.get("item_code")

        if subject == "product" and not item_code:
            raise serializers.ValidationError(
                {"item_code": "Item code is required for product enquiry."}
            )

        return data


class FabricListSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    product_category = serializers.CharField(source="product_category.name")

    class Meta:
        model = Fabric
        fields = ["id", "item_code", "product_category", "finish", "photo_url"]

    def get_photo_url(self, obj):
        if obj.photo and obj.photo.file:
            return obj.photo.file.url
        return None


class FabricSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    aux_photo1_url = serializers.SerializerMethodField()
    aux_photo2_url = serializers.SerializerMethodField()
    aux_photo3_url = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    related_fabrics = serializers.SerializerMethodField()
    product_category_name = serializers.CharField(source="product_category.name")

    class Meta:
        model = Fabric
        exclude = [
            "photo",
            "aux_photo1",
            "aux_photo2",
            "aux_photo3",
            "product_category",
        ]

    def get_photo_url(self, obj):
        if obj.photo and obj.photo.file:
            return obj.photo.file.url
        return None

    def get_aux_photo1_url(self, obj):
        if obj.aux_photo1 and obj.aux_photo1.file:
            return obj.aux_photo1.file.url
        return None

    def get_aux_photo2_url(self, obj):
        if obj.aux_photo2 and obj.aux_photo2.file:
            return obj.aux_photo2.file.url
        return None

    def get_aux_photo3_url(self, obj):
        if obj.aux_photo3 and obj.aux_photo3.file:
            return obj.aux_photo3.file.url
        return None

    def get_is_favorite(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, fabric=obj).exists()
        return False

    def get_related_fabrics(self, obj):
        user = self.context.get("request").user
        related_fabrics = []

        if user.is_authenticated:
            favorite_fabrics = Favorite.objects.filter(user=user).values_list(
                "fabric", flat=True
            )
            similar_to_favorites = (
                Fabric.objects.filter(
                    product_category__in=Fabric.objects.filter(
                        id__in=favorite_fabrics
                    ).values("product_category")
                )
                .exclude(id__in=favorite_fabrics)
                .distinct()
            )
            related_fabrics = list(similar_to_favorites[:8])

        if len(related_fabrics) < 8:
            remaining_slots = 8 - len(related_fabrics)
            similar_to_current = (
                Fabric.objects.filter(product_category=obj.product_category)
                .exclude(id=obj.id)
                .exclude(id__in=[fabric.id for fabric in related_fabrics])[
                    :remaining_slots
                ]
            )
            related_fabrics.extend(similar_to_current)

        return FabricListSerializer(related_fabrics[:8], many=True).data


class FavoriteSerializer(serializers.ModelSerializer):
    fabric = FabricSerializer()  # Serializer for the associated Fabric

    class Meta:
        model = Favorite
        fields = "__all__"  # Include all fields for Favorite


class OrderItemSerializer(serializers.ModelSerializer):
    fabric = FabricSerializer()  # Nest the FabricSerializer

    class Meta:
        model = OrderItem
        fields = ["id", "fabric", "color", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = UserUpdateSerializer()  # Include user data

    class Meta:
        model = Order
        fields = ["user", "order_date", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = validated_data.pop("user")
        user_instance = CustomUser.objects.get(id=user.id)
        order = Order.objects.create(user=user_instance, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class EventSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        extra_fields = ["photo_url"]
        # Include all fields except the 'photo' field explicitly
        exclude = ["photo"]

    def get_photo_url(self, obj):
        if obj.photo and obj.photo.file:
            return obj.photo.file.url
        return None


class BlogSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    author_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        extra_fields = ["photo_url", "author_photo_url"]
        # Include all fields except the 'photo' field explicitly
        exclude = ["photo"]

    def get_photo_url(self, obj):
        if obj.photo and obj.photo.file:
            return obj.photo.file.url
        return None

    def get_owner_photo_url(self, obj):
        if obj.author.photo and obj.author.photo.file:
            return obj.author.photo.file.url
        return None


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs["uid"]))
            self.user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise ValidationError(
                "Token expired. Please request a new password reset link"
            )

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise ValidationError(
                "Token expired. Please request a new password reset link"
            )

        return attrs

    def save(self):
        return self.set_password_form.save()


class CartItemSerializer(serializers.ModelSerializer):
    fabric_id = serializers.PrimaryKeyRelatedField(
        queryset=Fabric.objects.all(), write_only=True, source="fabric"
    )
    fabric = FabricSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "fabric", "color", "quantity", "cart", "fabric_id"]

    def __init__(self, *args, **kwargs):
        super(CartItemSerializer, self).__init__(*args, **kwargs)
        self.fields["cart"].required = False

    def to_internal_value(self, data):
        # Remove cart from the validated data if present
        data.pop("cart", None)
        return super(CartItemSerializer, self).to_internal_value(data)


# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Cart
#         fields = ["id", "user", "items"]
#         read_only_fields = ["user"]


class ContactRequestSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(read_only=True)
    related_fabric_details = serializers.SerializerMethodField()

    class Meta:
        model = ContactRequest
        fields = [
            "id",
            "user",
            "request_number",
            "subject",
            "message",
            "created_at",
            "company_name",
            "related_fabric_details",
        ]

    def get_related_fabric_details(self, obj):
        if obj.subject in ["product", "product_request"]:
            fabrics = obj.related_fabric.all()
            return FabricSerializer(fabrics, many=True, context=self.context).data

        return []
