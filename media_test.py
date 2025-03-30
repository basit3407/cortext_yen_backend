import os
import django
from django.conf import settings

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cortex_yen.settings')
django.setup()

# Print media settings
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"DEBUG: {settings.DEBUG}")

# Check if an image file exists
filepath = os.path.join(settings.MEDIA_ROOT, 'corlee', 'uploads', 'felipe-santana-xJkTCbtuqAY-unsplash.webp')
if os.path.exists(filepath):
    print(f"File exists at: {filepath}")
    print(f"File URL would be: {settings.MEDIA_URL + 'corlee/uploads/felipe-santana-xJkTCbtuqAY-unsplash.webp'}")
else:
    print(f"File does not exist at: {filepath}") 