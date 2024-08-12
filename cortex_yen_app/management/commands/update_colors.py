from django.core.management.base import BaseCommand

from cortex_yen_app.models import FabricColorCategory


class Command(BaseCommand):
    help = "Update color field to match display_name for existing records"

    def handle(self, *args, **kwargs):
        updated_count = 0
        for category in FabricColorCategory.objects.all():
            if not category.color:  # Only update if color is empty
                category.color = category.display_name
                category.save(update_fields=["color"])
                updated_count += 1
        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated {updated_count} records.")
        )
