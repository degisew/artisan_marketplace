"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# import csv
import os
import environ
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Take environment variables from .env file
env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=["*"])

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = "account.User"

ROOT_URLCONF = 'config.urls'

SHOW_SWAGGER = env("SHOW_SWAGGER", default=True, cast=bool)

ENV = env("ENV", default="development")

# A list of all the people who get code error notifications.
ADMINS=env('ADMINS')

CORS_ALLOW_ALL_ORIGINS = env(
    "CORS_ALLOW_ALL_ORIGINS", cast=bool, default=True
)

CSRF_TRUSTED_ORIGINS = env(
    "CSRF_TRUSTED_ORIGINS", default=["*"]
)

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'rest_access_policy',
    'drf_standardized_errors',

]

CUSTOM_APPS = [
    'apps.core',
    'apps.account',
    'apps.store'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

# middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


if not DEBUG:
    ADMIN_URL = env("ADMIN_URL", default="supersecretadmin/")
else:
    ADMIN_URL = env("ADMIN_URL", default="admin/")


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env("TIME_ZONE", cast=str)

USE_TZ = env("USE_TZ", cast=bool)

USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

DATALOOKUP_MODEL = "core.DataLookup"

POLICIES_FILE_PATH = env(
    "ACCESS_POLICY_FILE",
    default=os.path.join(BASE_DIR, "config", "policies.json"),
    cast=str,
)

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    # default exception formatter
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}

DRF_STANDARDIZED_ERRORS = {"ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True}

SIMPLE_JWT = {
    "AUTH_TOKEN_CLASSES": ["rest_framework_simplejwt.tokens.AccessToken"],
    "ACCESS_TOKEN_LIFETIME": (
        timedelta(hours=1) if not DEBUG else timedelta(days=30)
    ),
    "REFRESH_TOKEN_LIFETIME": (
        timedelta(days=1) if not DEBUG else timedelta(days=30)
    ),
    "USER_ID_FIELD": "id",
    "TOKEN_REFRESH_SERIALIZER": "authn.serializers.TokenRefreshSerializer",
    "ROTATE_REFRESH_TOKENS": True,
}

SPECTACULAR_SETTINGS = {
    "TITLE": _(env("APP_TITLE", cast=str)),
    "DESCRIPTION": _(env("APP_DESCRIPTION", cast=str)),
    'VERSION': '1.0.0',
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
