from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.utils.crypto import get_random_string
from .validators import validate_colors


class MediaUploads(models.Model):
    file = models.FileField(upload_to="corlee/uploads/")


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

    def __str__(self):
        return self.username


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Fabric(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    photo = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="fabric_photos",
        null=True,
        blank=True,
    )
    aux_photo1 = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="aux_photo1",
        null=True,
        blank=True,
    )
    aux_photo2 = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="aux_photo2",
        null=True,
        blank=True,
    )
    aux_photo3 = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="aux_photo3",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=100)
    composition = models.CharField(max_length=255)
    weight = models.CharField(max_length=100)
    finish = models.CharField(max_length=100)
    available_colors = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        default=list,
        validators=[validate_colors],
    )
    item_code = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hot_selling = models.BooleanField(default=False)

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
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
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
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)  # New field for tracking views
    photo = models.ForeignKey(
        MediaUploads,
        on_delete=models.DO_NOTHING,
        related_name="blog_photos",
        null=True,
        blank=True,
    )
    tags = models.CharField(max_length=255)
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
    sample_requested = models.BooleanField(default=False)
    related_order = models.ForeignKey(
        Order, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Request {self.request_number} by {self.user.username}"

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
