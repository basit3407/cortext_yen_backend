# Generated by Django 5.0.4 on 2024-06-20 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0003_remove_mediauploads_caption_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="auth_method",
            field=models.CharField(
                choices=[("google", "Google"), ("email", "Email")],
                default="email",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
