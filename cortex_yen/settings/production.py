from .base import *
import os


DEBUG = False

ALLOWED_HOSTS = ["corleebackend-05d62e3e59f9.herokuapp.com"]

# Ensure you add any other production-specific settings here


# SendGrid settings
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = (
    "apikey"  # This is the string literal "apikey", not the API key itself
)
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
DEFAULT_FROM_EMAIL = "support@corleeandco.com"
