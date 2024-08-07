from django.core.management.base import BaseCommand
from cortex_yen_app.models import MediaUploads
import re
import boto3
from botocore.exceptions import ClientError
from urllib.parse import urlparse


class Command(BaseCommand):
    help = "Update image URLs to use .webp extensions"

    def handle(self, *args, **kwargs):
        # Regex pattern to match the old image extensions
        pattern = re.compile(r"\.(jpeg|png|jpg|jfif)$", re.IGNORECASE)

        # Initialize the S3 client
        s3 = boto3.client("s3")

        # Get all instances of the MediaUploads model
        instances = MediaUploads.objects.all()

        for instance in instances:
            if instance.file:
                old_url = instance.file.url

                # Parse the old URL to extract bucket name and object key
                parsed_url = urlparse(old_url)
                bucket_name = "corleeandcobackend"
                old_key = parsed_url.path.lstrip("/")

                # Construct new key
                new_key = pattern.sub(".webp", old_key)
                new_url = f"https://{parsed_url.netloc}/{new_key}"

                # Debugging outputs
                self.stdout.write(self.style.NOTICE(f"Old URL: {old_url}"))
                self.stdout.write(self.style.NOTICE(f"New URL: {new_url}"))
                self.stdout.write(self.style.NOTICE(f"Bucket Name: {bucket_name}"))
                self.stdout.write(self.style.NOTICE(f"Old Key: {old_key}"))
                self.stdout.write(self.style.NOTICE(f"New Key: {new_key}"))

                try:
                    # Check if the new file exists in S3
                    s3.head_object(Bucket=bucket_name, Key=new_key)
                    # Update the field if the file exists
                    instance.file.name = new_key
                    instance.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updated URL for {instance} from {old_url} to {new_url}"
                        )
                    )
                except ClientError as e:
                    self.stdout.write(
                        self.style.ERROR(f"File not found: {new_url}, Error: {e}")
                    )

        self.stdout.write(self.style.SUCCESS("All image URLs processed"))
