# Generated by Django 5.0.4 on 2024-07-28 13:21

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0018_auto_20240728_1644"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="content",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Text"),
        ),
    ]
