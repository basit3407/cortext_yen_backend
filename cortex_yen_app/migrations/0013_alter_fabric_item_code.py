# Generated by Django 5.0.4 on 2024-07-26 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "cortex_yen_app",
            "0012_remove_order_created_at_remove_order_customer_email_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="fabric",
            name="item_code",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
