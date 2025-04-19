from unicodedata import category
from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.crypto import get_random_string
from .validators import validate_colors
from django.core.validators import RegexValidator
from PIL import Image
import os
from django.core.files.base import ContentFile
from io import BytesIO


class MediaUploads(models.Model):
    file = models.FileField(upload_to="corlee/uploads/", max_length=255)

    def save(self, *args, **kwargs):
        # Open the uploaded image
        img = Image.open(self.file)

        # Initialize output buffer
        output = BytesIO()

        # Always convert and optimize the image
        img.save(output, format="WEBP", quality=85)
        output.seek(0)

        # Change the file field to the new image with proper content type
        self.file = ContentFile(
            output.read(), 
            name=os.path.splitext(self.file.name)[0] + ".webp"
        )
        self.file.content_type = 'image/webp'  # Set the correct content type

        super().save(*args, **kwargs)


class FabricColorCategory(models.Model):
    display_name = models.CharField(max_length=255)
    color = models.CharField(
        max_length=255, validators=[validate_colors], blank=True, null=True
    )

    def __str__(self):
        return self.display_name

    def delete(self, *args, **kwargs):
        # Check if this color category is being used by any fabric color images
        fabric_count = self.colors.count()
        if fabric_count > 0:
            raise ValidationError(
                f"This color category cannot be deleted since it is being used in {fabric_count} product(s)."
            )
        super().delete(*args, **kwargs)


class FabricColorImage(models.Model):
    fabric = models.ForeignKey(
        "Fabric", on_delete=models.CASCADE, related_name="color_images"
    )
    color_category = models.ForeignKey(
        FabricColorCategory, related_name="colors", on_delete=models.SET_NULL, null=True
    )
    primary_image = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="primary_images",
        null=False,
        blank=False,
        default=1  # This will be used for existing records
    )
    aux_image1 = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="aux_image1",
        null=True,
        blank=True,
    )
    aux_image2 = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="aux_image2",
        null=True,
        blank=True,
    )
    aux_image3 = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="aux_image3",
        null=True,
        blank=True,
    )
    model_image = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="model_image",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.color_category.display_name} images for {self.fabric.title}"


class CustomUser(AbstractUser):
    AUTH_METHOD_CHOICES = (
        ("google", "Google"),
        ("email", "Email"),
    )

    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="user_photos",
        null=True,
        blank=True,
    )
    auth_method = models.CharField(
        max_length=10, choices=AUTH_METHOD_CHOICES, default="email"
    )

    def generate_verification_token(self):
        token = get_random_string(length=32)
        self.verification_token = token
        self.save()
        return token

    def verify_email(self):
        self.is_verified = True
        self.verification_token = None
        self.save()

    def delete(self, *args, **kwargs):
        # Delete all related records first
        # Delete orders (this will cascade delete order items due to CASCADE on_delete)
        self.order_set.all().delete()
        
        # Delete favorites
        self.favorite_set.all().delete()
        
        # Delete contact requests
        self.contactrequest_set.all().delete()
        
        # Delete cart and cart items
        if hasattr(self, 'cart'):
            self.cart.items.all().delete()
            self.cart.delete()
        
        # Delete blogs authored by the user
        self.blog_set.all().delete()
        
        # Finally delete the user
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ForeignKey(
        MediaUploads, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Check if this category is being used by any fabrics
        fabric_count = self.fabric_set.count()
        if fabric_count > 0:
            raise ValidationError(
                f"This product category cannot be deleted since it is being used in {fabric_count} product(s)."
            )
        super().delete(*args, **kwargs)


class Fabric(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=100)
    composition = models.CharField(max_length=255)
    weight = models.CharField(max_length=100)
    finish = models.CharField(max_length=100)
    item_code = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]*$",
                message="Item code must contain only letters and numbers.",
                code="invalid_item_code",
            )
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_hot_selling = models.BooleanField(default=False)

    def validate_color_images(self):
        if not self.color_images.exists():
            raise ValidationError(
                "You must add at least one color along with the primary image."
            )

    def delete(self, *args, **kwargs):
        # Check if this fabric is being used in any orders
        order_count = self.orderitem_set.count()
        if order_count > 0:
            raise ValidationError(
                f"This fabric cannot be deleted since it is being used in {order_count} order(s)."
            )
        
        # Check if this fabric is being used in any contact requests
        contact_request_count = self.contactrequest_set.count()
        if contact_request_count > 0:
            raise ValidationError(
                f"This fabric cannot be deleted since it is being used in {contact_request_count} contact request(s)."
            )
        
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "fabric")

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.fabric.title}"


class Order(models.Model):
    fabrics = models.ManyToManyField(Fabric, through="OrderItem")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    fabric = models.ForeignKey(
        Fabric, on_delete=models.CASCADE, related_name="orderitem_set", null=True, blank=True
    )
    color = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order} - {self.fabric}"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    photo = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="event_photos",
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=255)
    url = models.URLField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = content = CKEditor5Field(
        "Text", config_name="default"
    )  # Use CKEditor5Field
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)  # New field for tracking views
    photo = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="blog_photos",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="cart"
    )

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.fabric.title} ({self.color}) - {self.quantity}"


class ContactRequest(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
        ("pending", "Pending"),
    ]

    ORDER_STATUS_CHOICES = [
        ("new", "New"),
        ("processing", "Processing"),
        ("dispatched", "Dispatched"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("returned", "Returned"),
    ]

    REQUEST_TYPE_CHOICES = [
        ("general", "General Inquiry"),
        ("product", "Product Inquiry"),
        ("product_request", "Product Request"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    request_number = models.CharField(max_length=12, blank=True)
    request_type = models.CharField(
        max_length=255, choices=REQUEST_TYPE_CHOICES, default="general"
    )
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    related_fabric = models.ForeignKey(
        Fabric, null=True, blank=True, on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    sample_requested = models.BooleanField(default=False)
    related_order = models.ForeignKey(
        Order, null=True, blank=True, on_delete=models.CASCADE
    )

    current_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new"
    )
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="new"
    )

    def __str__(self):
        if self.user:
            return f"Request {self.request_number} by {self.user.username}"
        return f"Request {self.request_number} (No User)"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(ContactRequest, self).save(*args, **kwargs)
        if is_new:
            if not self.request_number:
                self.request_number = self.generate_request_number()
                self.save()

    def generate_request_number(self):
        random_str = get_random_string(
            length=5, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )
        return f"{self.id}{random_str}"


class ContactDetails(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=24.0708)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=120.5409)
    country = models.CharField(max_length=50)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    whatsapp = models.CharField(blank=True, null=True, max_length=255)
    line = models.CharField(blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk and ContactDetails.objects.exists():
            raise ValidationError(
                "There is already a ContactDetails instance. Only one instance is allowed."
            )
        return super(ContactDetails, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
