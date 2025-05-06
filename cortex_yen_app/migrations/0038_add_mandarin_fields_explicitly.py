from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('cortex_yen_app', '0037_remove_fabriccolorimage_color_contactrequest_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabric',
            name='title_mandarin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='description_mandarin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='composition_mandarin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='weight_mandarin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='finish_mandarin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ] 