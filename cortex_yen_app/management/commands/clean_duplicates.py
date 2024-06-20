# cortex_yen_app/management/commands/clean_duplicates.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from cortex_yen_app.models import CustomUser


class Command(BaseCommand):
    help = "Clean up duplicate emails in CustomUser table"

    def handle(self, *args, **kwargs):
        duplicates = (
            CustomUser.objects.values("email")
            .annotate(email_count=Count("email"))
            .filter(email_count__gt=1)
        )

        with transaction.atomic():
            for entry in duplicates:
                email = entry["email"]
                users = CustomUser.objects.filter(email=email)
                for i, user in enumerate(users):
                    if i > 0:  # Keep the first one as is
                        new_email = f"{user.email}_{i}"
                        self.stdout.write(
                            self.style.WARNING(
                                f"Updating email for user {user.id}: {user.email} -> {new_email}"
                            )
                        )
                        user.email = new_email
                        user.save()

        self.stdout.write(self.style.SUCCESS("Duplicate emails have been cleaned up"))
