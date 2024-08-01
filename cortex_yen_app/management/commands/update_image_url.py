from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

MEDIA_URL = settings.MEDIA_URL


from cortex_yen_app.models import MediaUploads


class Command(BaseCommand):
    help = "Update image URLs to use CloudFront"

    def handle(self, *args, **kwargs):
        OLD_BUCKET_URL = (
            "https://your-bucket-name.s3.ap-southeast-1.amazonaws.com/corlee/uploads/"
        )
        NEW_CLOUDFRONT_URL = "https://d1emfok2hfg9f.cloudfront.net/corlee/uploads/"

        @transaction.atomic
        def update_media_urls():
            for instance in MediaUploads.objects.all():
                if instance.file:
                    new_url = instance.file.url.replace(
                        OLD_BUCKET_URL, NEW_CLOUDFRONT_URL
                    )
                    instance.file.name = new_url.replace(
                        MEDIA_URL, ""
                    )  # Update the file name to the new path
                    instance.save()

        update_media_urls()
        self.stdout.write(self.style.SUCCESS("Successfully updated image URLs"))
