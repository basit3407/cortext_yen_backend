# Generated by Django 5.0.4 on 2024-07-27 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0015_blog_view_count"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blog",
            old_name="tags",
            new_name="category",
        ),
    ]
