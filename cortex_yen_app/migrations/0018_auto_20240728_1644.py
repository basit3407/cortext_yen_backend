import django.db.models.deletion
from django.db import migrations, models


def create_categories_and_update_blogs(apps, schema_editor):
    Blog = apps.get_model("cortex_yen_app", "Blog")
    BlogCategory = apps.get_model("cortex_yen_app", "BlogCategory")

    # Create categories
    categories = Blog.objects.values_list("category_temp", flat=True).distinct()
    category_mapping = {}
    for category in categories:
        if category:
            new_category, created = BlogCategory.objects.get_or_create(name=category)
            category_mapping[category] = new_category

    # Update blogs with the new category
    for blog in Blog.objects.all():
        if blog.category_temp in category_mapping:
            blog.category = category_mapping[blog.category_temp]
            blog.save()


class Migration(migrations.Migration):

    dependencies = [
        (
            "cortex_yen_app",
            "0017_auto_20240728_1643",
        ),  # Update with your previous migration name
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
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
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="blog",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="cortex_yen_app.BlogCategory",
            ),
        ),
        migrations.RunPython(create_categories_and_update_blogs),
        migrations.RemoveField(
            model_name="blog",
            name="category_temp",
        ),
        migrations.AlterField(
            model_name="blog",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="cortex_yen_app.BlogCategory",
            ),
        ),
    ]
