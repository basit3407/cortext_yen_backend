import os

# Import production settings if DJANGO_SETTINGS_MODULE is set to production
# Otherwise, import local settings for development
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'cortex_yen.settings.production':
    from .production import *
else:
    from .local import *
