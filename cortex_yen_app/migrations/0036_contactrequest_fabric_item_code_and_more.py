# Generated by Django 5.0.4 on 2025-03-26 03:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cortex_yen_app', '0035_fabriccolorimage_model_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_item_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='color_images',
            field=models.ManyToManyField(through='cortex_yen_app.FabricColorImage', to='cortex_yen_app.fabriccolorcategory'),
        ),
        migrations.AddField(
            model_name='fabric',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='mediauploads',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='mediauploads',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='related_fabric',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cortex_yen_app.fabric'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='composition',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='item_code',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fabrics', to='cortex_yen_app.productcategory'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='fabriccolorimage',
            name='aux_image1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aux1_fabric_images', to='cortex_yen_app.mediauploads'),
        ),
        migrations.AlterField(
            model_name='fabriccolorimage',
            name='aux_image2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aux2_fabric_images', to='cortex_yen_app.mediauploads'),
        ),
        migrations.AlterField(
            model_name='fabriccolorimage',
            name='aux_image3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aux3_fabric_images', to='cortex_yen_app.mediauploads'),
        ),
        migrations.AlterField(
            model_name='fabriccolorimage',
            name='color_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fabric_images_through', to='cortex_yen_app.fabriccolorcategory'),
        ),
        migrations.AlterField(
            model_name='fabriccolorimage',
            name='fabric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_images_through', to='cortex_yen_app.fabric'),
        ),
        migrations.AlterField(
            model_name='fabriccolorimage',
            name='model_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='model_fabric_images', to='cortex_yen_app.mediauploads'),
        ),
        migrations.AlterField(
            model_name='fabriccolorimage',
            name='primary_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_fabric_images', to='cortex_yen_app.mediauploads'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='fabric',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='cortex_yen_app.fabric'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='fabriccolorimage',
            unique_together={('fabric', 'color_category')},
        ),
    ]
