# Generated by Django 5.0.4 on 2025-05-05 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cortex_yen_app', '0042_remove_unused_mandarin_fields'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='productcategory',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
