# Generated manually

from django.db import migrations, models
import django.db.models.deletion


def clean_migration_fix(apps, schema_editor):
    """
    This function will fix all migration issues by:
    1. Ensuring all required columns exist in the database
    2. Fixing any foreign key constraints
    3. Handling any data migrations needed
    """
    if schema_editor.connection.vendor == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            # First, check and drop any existing foreign key constraints that might conflict
            cursor.execute("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'cortex_yen_app_fabriccolorimage'
                AND constraint_type = 'FOREIGN KEY'
                AND constraint_name LIKE '%model_image%';
            """)
            for constraint in cursor.fetchall():
                schema_editor.execute(f'ALTER TABLE cortex_yen_app_fabriccolorimage DROP CONSTRAINT IF EXISTS {constraint[0]};')

            # Check for existing unique constraints
            cursor.execute("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'cortex_yen_app_fabriccolorimage'
                AND constraint_type = 'UNIQUE'
                AND constraint_name LIKE '%fabric_id_color_category%';
            """)
            existing_constraints = cursor.fetchall()
            
            # If unique constraint exists, drop it
            for constraint in existing_constraints:
                schema_editor.execute(f'ALTER TABLE cortex_yen_app_fabriccolorimage DROP CONSTRAINT IF EXISTS {constraint[0]};')

            # Now check and handle each table's columns
            tables_and_columns = {
                'cortex_yen_app_fabriccolorimage': [
                    ('model_image_id', 'bigint NULL')
                ],
                'cortex_yen_app_contactrequest': [
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
                ],
                'cortex_yen_app_orderitem': [
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
                ],
                'cortex_yen_app_fabric': [
                    ('updated_at', 'TIMESTAMP WITH TIME ZONE')
                ],
                'cortex_yen_app_mediauploads': [
                    ('created_at', 'TIMESTAMP WITH TIME ZONE'),
                    ('updated_at', 'TIMESTAMP WITH TIME ZONE')
                ]
            }

            for table, columns in tables_and_columns.items():
                for column, column_type in columns:
                    # Check if column exists
                    cursor.execute(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name='{table}' 
                        AND column_name='{column}';
                    """)
                    if not cursor.fetchone():
                        try:
                            schema_editor.execute(f'ALTER TABLE {table} ADD COLUMN {column} {column_type};')
                        except Exception as e:
                            # If column already exists or other error, log it but continue
                            print(f"Error adding column {column} to {table}: {str(e)}")
                            continue

            # Add foreign key constraint for model_image_id if it doesn't exist
            cursor.execute("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'cortex_yen_app_fabriccolorimage'
                AND constraint_type = 'FOREIGN KEY'
                AND constraint_name LIKE '%model_image%';
            """)
            if not cursor.fetchone():
                try:
                    schema_editor.execute("""
                        ALTER TABLE cortex_yen_app_fabriccolorimage 
                        ADD CONSTRAINT cortex_yen_app_fabriccolorimage_model_image_id_fkey 
                        FOREIGN KEY (model_image_id) 
                        REFERENCES cortex_yen_app_mediauploads(id) 
                        ON DELETE SET NULL;
                    """)
                except Exception as e:
                    print(f"Error adding foreign key constraint: {str(e)}")

            # Add unique constraint if it doesn't exist
            cursor.execute("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'cortex_yen_app_fabriccolorimage'
                AND constraint_type = 'UNIQUE'
                AND constraint_name LIKE '%fabric_id_color_category%';
            """)
            if not cursor.fetchone():
                try:
                    schema_editor.execute("""
                        CREATE UNIQUE INDEX cortex_yen_app_fabriccol_fabric_id_color_category_9cbcd810_uniq 
                        ON cortex_yen_app_fabriccolorimage (fabric_id, color_category_id);
                    """)
                except Exception as e:
                    print(f"Error adding unique constraint: {str(e)}")


def reverse_migration(apps, schema_editor):
    """
    Reverse migration - we don't want to drop columns as they might contain data
    """
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('cortex_yen_app', '0034_remove_fabriccolorimage_color'),
    ]

    operations = [
        # Run the Python code to ensure all columns exist and constraints are correct
        migrations.RunPython(clean_migration_fix, reverse_code=reverse_migration),
    ] 