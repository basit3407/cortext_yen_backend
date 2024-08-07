from django.core.management.base import BaseCommand
from cortex_yen_app.models import MediaUploads
import re


class Command(BaseCommand):
    help = "Update image URLs to use .webp extensions"

    def handle(self, *args, **kwargs):
        # Regex pattern to match the old image extensions
        pattern = re.compile(r"\.(jpeg|png|jpg|jfif)$", re.IGNORECASE)

        # Get all instances of the MediaUploads model
        instances = MediaUploads.objects.all()

        for instance in instances:
            if instance.file:
                # Replace the old extensions with .webp
                new_url = pattern.sub(".webp", instance.file.url)
                # Use instance.file.name to update the field
                instance.file.name = new_url
                instance.save()
                self.stdout.write(self.style.SUCCESS(f"Updated URL for {instance}"))

        self.stdout.write(self.style.SUCCESS("All image URLs updated successfully"))
