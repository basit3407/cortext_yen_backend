from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Blog,
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


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "description"]


class ContactFormSerializer(serializers.Serializer):
    item_code = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    subject = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    company_name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)


class FabricSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Fabric
        extra_fields = ["photo_url"]
        # Include all fields except the 'photo' field explicitly
        exclude = ["photo"]

    def get_photo_url(self, obj):
        if obj.photo and obj.photo.file:
            return obj.photo.file.url
        return None


class FavoriteSerializer(serializers.ModelSerializer):
    fabric = FabricSerializer()  # Serializer for the associated Fabric

    class Meta:
        model = Favorite
        fields = "__all__"  # Include all fields for Favorite


class OrderItemSerializer(serializers.ModelSerializer):
    fabric = FabricSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"


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
