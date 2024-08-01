from pathlib import Path
import os
import django_heroku
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-hs(!v78=x_s_d=wm2v(otb%f&oj!%trz@h%xbv6t6(jv+3z76n",
)

DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "cortex_yen_app.CustomUser"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cortex_yen_app",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "storages",
    "corsheaders",
    "django_ckeditor_5",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": 8,  # The default page size if not otherwise specified
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    }
}

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "cortex_yen.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cortex_yen.wsgi.application"

if "DATABASE_URL" in os.environ:
    DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}
else:
    DATABASES = {}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

django_heroku.settings(locals())

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

FRONTEND_URL = "www.corleeandco.com"


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = "d1emfok2hfg9f.cloudfront.net"


AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

# Static files (CSS, JavaScript, Images)
STATIC_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Media files
MEDIA_LOCATION = "corlee/uploads"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload",
            "|",
            "fontFamily",
            "fontSize",
            "fontColor",
            "fontBackgroundColor",
            "|",
            "alignment",
            "outdent",
            "indent",
            "|",
            "insertTable",
            "mediaEmbed",
            "undo",
            "redo",
        ],
        "height": 300,
        "width": "auto",
        "fontFamily": {
            "options": [
                "default",
                "Arial, Helvetica, sans-serif",
                "Courier New, Courier, monospace",
                "Georgia, serif",
                "Lucida Sans Unicode, Lucida Grande, sans-serif",
                "Tahoma, Geneva, sans-serif",
                "Times New Roman, Times, serif",
                "Trebuchet MS, Helvetica, sans-serif",
                "Verdana, Geneva, sans-serif",
            ],
        },
        "fontSize": {
            "options": [
                "8",
                "10",
                "12",
                "14",
                "16",
                "18",
                "20",
                "24",
                "28",
                "32",
                "36",
                "40",
                "48",
            ],
            "supportAllValues": True,
        },
        "fontColor": {
            "columns": 5,
            "documentColors": 10,
        },
        "fontBackgroundColor": {
            "columns": 5,
            "documentColors": 10,
        },
        "alignment": {
            "options": ["left", "right", "center", "justify"],
        },
    }
}


from django.db import transaction

OLD_BUCKET_URL = "https://corleebe.s3.ap-southeast-1.amazonaws.com/corlee/uploads/"
NEW_CLOUDFRONT_URL = "https://d1emfok2hfg9f.cloudfront.net/corlee/uploads/"
