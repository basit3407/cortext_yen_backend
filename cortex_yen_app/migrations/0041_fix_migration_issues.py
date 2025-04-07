# Generated manually

from django.db import migrations, models
import django.db.models.deletion


def fix_migration_issues(apps, schema_editor):
    """
    This function will fix all migration issues by:
    1. Ensuring the model_image field exists in FabricColorImage
    2. Adding any missing columns to the database
    3. Fixing any foreign key constraints
    """
    if schema_editor.connection.vendor == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            # Check if model_image_id column exists in FabricColorImage
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='cortex_yen_app_fabriccolorimage' 
                AND column_name='model_image_id';
            """)
            if not cursor.fetchone():
                # Add the column if it doesn't exist
                schema_editor.execute('ALTER TABLE cortex_yen_app_fabriccolorimage ADD COLUMN model_image_id bigint NULL;')
                # Add the foreign key constraint
                schema_editor.execute('ALTER TABLE cortex_yen_app_fabriccolorimage ADD CONSTRAINT cortex_yen_app_fabriccolorimage_model_image_id_fkey FOREIGN KEY (model_image_id) REFERENCES cortex_yen_app_mediauploads(id) ON DELETE NO ACTION;')
            
            # Check for other missing columns in ContactRequest
            contact_request_columns = [
                ('fabric_item_code', 'VARCHAR(100)'),
                ('fabric_title', 'VARCHAR(200)'),
                ('fabric_category_name', 'VARCHAR(100)'),
                ('fabric_composition', 'VARCHAR(200)'),
                ('fabric_description', 'TEXT'),
                ('fabric_finish', 'VARCHAR(100)'),
                ('fabric_is_hot_selling', 'BOOLEAN'),
                ('fabric_weight', 'VARCHAR(50)'),
                ('fabric_colors', 'TEXT'),
                ('fabric_created_at', 'TIMESTAMP WITH TIME ZONE'),
                ('fabric_images', 'TEXT'),
                ('fabric_updated_at', 'TIMESTAMP WITH TIME ZONE'),
                ('name', 'VARCHAR(100)'),
                ('phone', 'VARCHAR(20)')
            ]
            
            for column, column_type in contact_request_columns:
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='cortex_yen_app_contactrequest' 
                    AND column_name='{column}';
                """)
                if not cursor.fetchone():
                    schema_editor.execute(f'ALTER TABLE cortex_yen_app_contactrequest ADD COLUMN {column} {column_type};')
            
            # Check for missing columns in OrderItem
            order_item_columns = [
                ('fabric_title', 'VARCHAR(200)'),
                ('item_code', 'VARCHAR(100)'),
                ('fabric_category_name', 'VARCHAR(100)'),
                ('fabric_composition', 'VARCHAR(200)'),
                ('fabric_description', 'TEXT'),
                ('fabric_finish', 'VARCHAR(100)'),
                ('fabric_is_hot_selling', 'BOOLEAN'),
                ('fabric_weight', 'VARCHAR(50)'),
                ('aux_image1_url', 'VARCHAR(255)'),
                ('aux_image2_url', 'VARCHAR(255)'),
                ('aux_image3_url', 'VARCHAR(255)'),
                ('color_category_color', 'VARCHAR(100)'),
                ('color_category_name', 'VARCHAR(100)'),
                ('fabric_created_at', 'TIMESTAMP WITH TIME ZONE'),
                ('fabric_updated_at', 'TIMESTAMP WITH TIME ZONE'),
                ('model_image_url', 'VARCHAR(255)'),
                ('primary_image_url', 'VARCHAR(255)')
            ]
            
            for column, column_type in order_item_columns:
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='cortex_yen_app_orderitem' 
                    AND column_name='{column}';
                """)
                if not cursor.fetchone():
                    schema_editor.execute(f'ALTER TABLE cortex_yen_app_orderitem ADD COLUMN {column} {column_type};')
            
            # Check for missing columns in Fabric
            fabric_columns = [
                ('updated_at', 'TIMESTAMP WITH TIME ZONE')
            ]
            
            for column, column_type in fabric_columns:
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='cortex_yen_app_fabric' 
                    AND column_name='{column}';
                """)
                if not cursor.fetchone():
                    schema_editor.execute(f'ALTER TABLE cortex_yen_app_fabric ADD COLUMN {column} {column_type};')
            
            # Check for missing columns in MediaUploads
            media_uploads_columns = [
                ('created_at', 'TIMESTAMP WITH TIME ZONE'),
                ('updated_at', 'TIMESTAMP WITH TIME ZONE')
            ]
            
            for column, column_type in media_uploads_columns:
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='cortex_yen_app_mediauploads' 
                    AND column_name='{column}';
                """)
                if not cursor.fetchone():
                    schema_editor.execute(f'ALTER TABLE cortex_yen_app_mediauploads ADD COLUMN {column} {column_type};')


class Migration(migrations.Migration):

    dependencies = [
        ('cortex_yen_app', '0040_contactrequest_name_contactrequest_phone'),
    ]

    operations = [
        migrations.RunPython(fix_migration_issues, reverse_code=migrations.RunPython.noop),
        # Add the model_image field to FabricColorImage if it doesn't exist
        migrations.AddField(
            model_name='fabriccolorimage',
            name='model_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='model_fabric_images', to='cortex_yen_app.mediauploads'),
        ),
        # Add all the fields to ContactRequest
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
            model_name='contactrequest',
            name='fabric_category_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_composition',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_finish',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_is_hot_selling',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_weight',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_colors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_images',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='fabric_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        # Add all the fields to OrderItem
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
        migrations.AddField(
            model_name='orderitem',
            name='fabric_category_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_composition',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_finish',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_is_hot_selling',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_weight',
            field=models.CharField(blank=True, max_length=50, null=True),
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
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='color_category_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='fabric_updated_at',
            field=models.DateTimeField(blank=True, null=True),
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
        # Add fields to Fabric
        migrations.AddField(
            model_name='fabric',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        # Add fields to MediaUploads
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
    ] 