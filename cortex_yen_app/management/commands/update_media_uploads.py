from django.core.management.base import BaseCommand

from cortex_yen_app.models import MediaUploads, ProductCategory


class Command(BaseCommand):
    help = "Update MediaUploads object with a specific primary key"

    def handle(self, *args, **kwargs):
        # Assuming the file is located at media/corlee/uploads/example.jpg
        file_path = "corlee/uploads/div__1ku4mui_253c17.png"

        # Step 1: Create a new MediaUploads object with the desired primary key (69)
        new_media_upload, created = MediaUploads.objects.get_or_create(
            id=69, defaults={"file": file_path}
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS("Created new MediaUploads object with ID 69")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("MediaUploads object with ID 69 already exists")
            )

        # Step 2: Update any related objects to point to the new MediaUploads object
        old_media_upload = MediaUploads.objects.get(id=5)  # Assuming 5 is the old ID
        ProductCategory.objects.filter(image=old_media_upload).update(
            image=new_media_upload
        )

        # Step 3: Delete the old MediaUploads object
        old_media_upload.delete()
        self.stdout.write(
            self.style.SUCCESS("Deleted old MediaUploads object with ID 5")
        )
