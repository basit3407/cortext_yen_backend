# Generated by Django 5.0.4 on 2024-07-22 06:40

import cortex_yen_app.validators
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0008_contactrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fabric",
            name="available_colors",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                size=None,
                validators=[cortex_yen_app.validators.validate_colors],
            ),
        ),
    ]
