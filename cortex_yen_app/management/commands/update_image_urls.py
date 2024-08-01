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
                    # Correct the URL to include 'corlee/uploads/'
                    if not old_url.startswith(NEW_CLOUDFRONT_URL):
                        new_url = NEW_CLOUDFRONT_URL + instance.file.name.split("/")[-1]
                        instance.file.name = (
                            "corlee/uploads/" + instance.file.name.split("/")[-1]
                        )
                    else:
                        new_url = old_url.replace(
                            settings.MEDIA_URL, NEW_CLOUDFRONT_URL
                        )
                        instance.file.name = (
                            "corlee/uploads/" + instance.file.name.split("/")[-1]
                        )
                    instance.save()

        update_media_urls()
        self.stdout.write(self.style.SUCCESS("Successfully updated image URLs"))
