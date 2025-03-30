from django.core.management.base import BaseCommand
from cortex_yen_app.models import FabricColorCategory


class Command(BaseCommand):
    help = "Populate FabricColorCategory with predefined color names"

    def handle(self, *args, **options):
        color_names = [
            "red",
            "blue",
            "green",
            "yellow",
            "black",
            "white",
            "gray",
            "orange",
            "purple",
            "pink",
        ]

        for color in color_names:
            if not FabricColorCategory.objects.filter(category=color).exists():
                FabricColorCategory.objects.create(category=color)
                self.stdout.write(self.style.SUCCESS(f"Created category: {color}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Category already exists: {color}")
                )

        self.stdout.write(self.style.SUCCESS("Finished populating FabricColorCategory"))
