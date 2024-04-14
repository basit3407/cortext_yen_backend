from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)

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
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=100)
    composition = models.CharField(max_length=255)
    weight = models.CharField(max_length=100)
    finish = models.CharField(max_length=100)
    available_colors = models.CharField(max_length=255)
    item_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    order_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
