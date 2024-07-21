# Generated by Django 5.0.4 on 2024-07-21 07:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0007_cart_cartitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "request_number",
                    models.CharField(blank=True, max_length=12, unique=True),
                ),
                (
                    "subject",
                    models.CharField(
                        choices=[
                            ("general", "General Inquiry"),
                            ("product", "Product Inquiry"),
                            ("custom", "Customization Inquiry"),
                            ("order", "Order Inquiry"),
                            ("product_request", "Product Request"),
                            ("other", "Other"),
                        ],
                        max_length=255,
                    ),
                ),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("company_name", models.CharField(blank=True, max_length=255)),
                (
                    "related_fabric",
                    models.ManyToManyField(blank=True, to="cortex_yen_app.fabric"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]