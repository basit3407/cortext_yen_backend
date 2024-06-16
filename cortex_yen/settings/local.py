from .base import *

DEBUG = True

ALLOWED_HOSTS = []

# Local database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'corleedb',
        'USER': 'postgres',
        'PASSWORD': 'Kmha@3407',  # Use the password you set for the new user
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Any other local-specific settings
