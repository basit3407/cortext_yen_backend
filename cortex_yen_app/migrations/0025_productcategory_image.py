# Generated by Django 5.0.4 on 2024-08-01 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0024_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="productcategory",
            name="image",
            field=models.ForeignKey(
                default=69,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="cortex_yen_app.mediauploads",
            ),
        ),
    ]
