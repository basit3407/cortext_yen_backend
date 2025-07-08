from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cortex_yen_app', '0048_add_soft_delete_to_fabric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ] 