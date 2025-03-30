# Generated by Django 5.0.4 on 2024-08-12 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0028_fabriccolorcategory_fabriccolorimage_color_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactrequest",
            name="current_status",
            field=models.CharField(
                choices=[
                    ("new", "New"),
                    ("in_progress", "In Progress"),
                    ("resolved", "Resolved"),
                    ("closed", "Closed"),
                    ("pending", "Pending"),
                ],
                default="new",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contactrequest",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("new", "New"),
                    ("processing", "Processing"),
                    ("dispatched", "Dispatched"),
                    ("delivered", "Delivered"),
                    ("cancelled", "Cancelled"),
                    ("returned", "Returned"),
                ],
                default="new",
                max_length=20,
            ),
        ),
    ]
