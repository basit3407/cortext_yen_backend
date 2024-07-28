from django.db import migrations, models


def forwards(apps, schema_editor):
    Blog = apps.get_model("cortex_yen_app", "Blog")
    for blog in Blog.objects.all():
        blog.content = (
            blog.content
        )  # This line is just to trigger saving the same content
        blog.save()


def backwards(apps, schema_editor):
    # Reverse the migration logic if needed
    pass


class Migration(migrations.Migration):

    dependencies = [
        (
            "cortex_yen_app",
            "0019_alter_blog_content",
        ),  # Update with your previous migration name
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
