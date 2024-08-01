from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


class CortexYenAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cortex_yen_app"

    def ready(self):
        post_migrate.connect(run_update_urls, sender=self)


def run_update_urls(sender, **kwargs):
    call_command("update_image_urls")
