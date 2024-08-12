from django.core.management.base import BaseCommand
from cortex_yen_app.models import FabricColorImage, FabricColorCategory


class Command(BaseCommand):
    help = (
        "Update color_category for FabricColorImage instances based on the color field"
    )

    def handle(self, *args, **options):
        color_images = FabricColorImage.objects.all()
        updated_count = 0

        for image in color_images:
            if image.color:
                try:
                    color_category = FabricColorCategory.objects.get(
                        category=image.color
                    )
                    if image.color_category != color_category:
                        image.color_category = color_category
                        image.save()
                        updated_count += 1
                except FabricColorCategory.DoesNotExist:
                    # Optionally handle cases where the color does not match any category
                    image.color_category = None
                    image.save()

        self.stdout.write(
            self.style.SUCCESS(f"Updated {updated_count} FabricColorImage instances")
        )
