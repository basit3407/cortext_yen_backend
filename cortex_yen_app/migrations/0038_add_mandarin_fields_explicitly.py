from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('cortex_yen_app', '0037_remove_fabriccolorimage_color_contactrequest_name_and_more'),
    ]

    operations = [
        # This migration now uses RunSQL to make it safe even if fields were already added
        migrations.RunSQL(
            sql="""
                DO $$ 
                BEGIN
                    -- Check and add mandarin fields to Fabric if they don't exist
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                 WHERE table_name = 'cortex_yen_app_fabric' 
                                 AND column_name = 'title_mandarin') THEN
                        ALTER TABLE cortex_yen_app_fabric ADD COLUMN title_mandarin VARCHAR(255);
                    END IF;
                    
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                 WHERE table_name = 'cortex_yen_app_fabric' 
                                 AND column_name = 'description_mandarin') THEN
                        ALTER TABLE cortex_yen_app_fabric ADD COLUMN description_mandarin VARCHAR(100);
                    END IF;
                    
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                 WHERE table_name = 'cortex_yen_app_fabric' 
                                 AND column_name = 'composition_mandarin') THEN
                        ALTER TABLE cortex_yen_app_fabric ADD COLUMN composition_mandarin VARCHAR(255);
                    END IF;
                    
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                 WHERE table_name = 'cortex_yen_app_fabric' 
                                 AND column_name = 'weight_mandarin') THEN
                        ALTER TABLE cortex_yen_app_fabric ADD COLUMN weight_mandarin VARCHAR(100);
                    END IF;
                    
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                 WHERE table_name = 'cortex_yen_app_fabric' 
                                 AND column_name = 'finish_mandarin') THEN
                        ALTER TABLE cortex_yen_app_fabric ADD COLUMN finish_mandarin VARCHAR(100);
                    END IF;
                END $$;
            """,
            reverse_sql="-- No reverse operation needed",
        ),
    ] 