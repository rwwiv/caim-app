"""
Django settings for caim project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from glob import glob
from pathlib import Path

from django.contrib.messages import constants as messages

PRODUCTION = os.getenv("PRODUCTION", "0") == "1"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "0") == "1"
ALLOWED_HOSTS = ["*"]

APP_DIR = os.path.join(BASE_DIR, "caim_base")
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(APP_DIR, "static"))

# Cant use x-forwarded-host with cloudfront and apprunner
# so we do it via env vars
# USE_X_FORWARDED_HOST = True
URL_PREFIX = os.getenv("URL_PREFIX")

LOGIN_URL = "/login"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "csvexport",
    "leaflet",
    "sorl.thumbnail",  # Only needed for local dev - prod used imagekit.io
    "crispy_forms",
    "crispy_bootstrap5",
    "phonenumber_field",
    "avatar",
    "storages",
    "caim_base",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "caim.urls"

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
                "caim_base.context_processors.global_template_variables",
            ],
        },
    },
]

WSGI_APPLICATION = "caim.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        # "OPTIONS": {"options": "-c search_path=caim_dev,public"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
MEDIA_USE_S3 = os.getenv("MEDIA_USE_S3", "0") == "1"

if MEDIA_USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("MEDIA_AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    # s3 static settings
    AWS_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
    STATICFILES_STORAGE = "caim.storage_backends.StaticStorage"
    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "caim.storage_backends.PublicMediaStorage"
else:
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "static" / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_FAIL_SILENTLY = False

# Imagekit.io + cloudfront resizing
IMAGE_RESIZE_USE_IMAGKIT = os.getenv("IMAGE_RESIZE_USE_IMAGKIT", "0") == "1"
IMAGE_RESIZE_ORIGIN = os.getenv("IMAGE_RESIZE_ORIGIN", None)
IMAGE_RESIZE_CDN = os.getenv("IMAGE_RESIZE_CDN", None)


# Avatar
AVATAR_GRAVATAR_DEFAULT = "mp"
AVATAR_DEFAULT_URL = "/static/default_avatar.jpg"

if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {},
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            }
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "loggers": {
            # "django.db.backends": {
            #    "level": "DEBUG",
            #    "handlers": ["console"],
            # }
        },
    }

if not PRODUCTION:
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "https://staging.app.caim.org",
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        "https://app.caim.org",
    ]

if os.getenv("DOCKER"):
    GDAL_LIBRARY_PATH = glob("/usr/lib/libgdal.so.*")[0]
    GEOS_LIBRARY_PATH = glob("/usr/lib/libgeos_c.so.*")[0]


PHONENUMBER_DEFAULT_REGION = "US"
MAX_UPLOAD_SIZE = "5242880"


MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}


EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "0") == "1"

if EMAIL_ENABLED:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

TEMPLATED_EMAIL_TEMPLATE_DIR = "emails/"
TEMPLATED_EMAIL_FILE_EXTENSION = "email"
DEFAULT_FROM_EMAIL = "notifications@caim.org"

if PRODUCTION:
    GOOGLE_TAG_MANAGER_ID = "GTM-52CTCWP"
else:
    GOOGLE_TAG_MANAGER_ID = "GTM-NT67CZJ"


if sys.platform == 'darwin':
    import subprocess
    try:
        brew_prefix = subprocess.check_output(["brew", "--prefix"]).decode("utf-8").strip()
        GDAL_LIBRARY_PATH = f'{brew_prefix}/opt/gdal/lib/libgdal.dylib'
        GEOS_LIBRARY_PATH = f'{brew_prefix}/opt/geos/lib/libgeos_c.dylib'
    except subprocess.CalledProcessError:
        pass # brew not installed, assume libraries are in default location
