# Generated by Django 5.0.4 on 2025-03-26 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cortex_yen_app', '0037_contactrequest_fabric_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_colors',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_images',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='aux_image1_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='aux_image2_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='aux_image3_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='color_category_color',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='color_category_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='model_image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='primary_image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
