from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from cortex_yen_app.models import MediaUploads


class Command(BaseCommand):
    help = "Update image URLs to use CloudFront"

    def handle(self, *args, **kwargs):
        OLD_BUCKET_URL = (
            "https://corleeandcobackend.s3.ap-northeast-1.amazonaws.com/corlee/uploads/"
        )
        NEW_CLOUDFRONT_URL = "https://d1emfok2hfg9f.cloudfront.net/corlee/uploads/"

        @transaction.atomic
        def update_media_urls():
            for instance in MediaUploads.objects.all():
                if instance.file:
                    old_url = instance.file.url
                    # Check if the old URL format needs correction
                    if old_url.startswith(
                        "https://d1emfok2hfg9f.cloudfront.net/https%3A/"
                    ):
                        corrected_url = old_url.replace(
                            "https://d1emfok2hfg9f.cloudfront.net/https%3A/", "https://"
                        )
                        new_url = corrected_url.replace(
                            OLD_BUCKET_URL, NEW_CLOUDFRONT_URL
                        )
                    else:
                        new_url = old_url.replace(OLD_BUCKET_URL, NEW_CLOUDFRONT_URL)
                    # Update the file name to be relative to the MEDIA_URL
                    instance.file.name = new_url.replace(settings.MEDIA_URL, "")
                    instance.save()

        update_media_urls()
        self.stdout.write(self.style.SUCCESS("Successfully updated image URLs"))
