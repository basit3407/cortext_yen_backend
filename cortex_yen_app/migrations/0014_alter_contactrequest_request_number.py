# Generated by Django 5.0.4 on 2024-07-26 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0013_alter_fabric_item_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactrequest",
            name="request_number",
            field=models.CharField(blank=True, max_length=12),
        ),
    ]