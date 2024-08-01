# Generated by Django 5.0.4 on 2024-08-01 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0022_alter_mediauploads_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="fabric",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orderitem_set",
                to="cortex_yen_app.fabric",
            ),
        ),
    ]