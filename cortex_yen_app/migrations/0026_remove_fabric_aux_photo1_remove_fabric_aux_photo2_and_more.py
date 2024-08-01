# Generated by Django 5.0.4 on 2024-08-01 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cortex_yen_app", "0025_productcategory_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fabric",
            name="aux_photo1",
        ),
        migrations.RemoveField(
            model_name="fabric",
            name="aux_photo2",
        ),
        migrations.RemoveField(
            model_name="fabric",
            name="aux_photo3",
        ),
        migrations.RemoveField(
            model_name="fabric",
            name="available_colors",
        ),
        migrations.RemoveField(
            model_name="fabric",
            name="photo",
        ),
        migrations.CreateModel(
            name="FabricColorImage",
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
                ("color", models.CharField(max_length=50)),
                (
                    "aux_image1",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="aux_image1",
                        to="cortex_yen_app.mediauploads",
                    ),
                ),
                (
                    "aux_image2",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="aux_image2",
                        to="cortex_yen_app.mediauploads",
                    ),
                ),
                (
                    "aux_image3",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="aux_image3",
                        to="cortex_yen_app.mediauploads",
                    ),
                ),
                (
                    "fabric",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="color_images",
                        to="cortex_yen_app.fabric",
                    ),
                ),
                (
                    "primary_image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="primary_images",
                        to="cortex_yen_app.mediauploads",
                    ),
                ),
            ],
        ),
    ]
