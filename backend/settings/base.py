"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import json
from django.core import exceptions
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

try:
    with open(BASE_DIR / "backend/settings/secret.json", "r") as file:
        secret = json.load(file)
except:
    secret = {}


def get_var(key, secret=secret):
    try:
        value = os.environ[key]
    except KeyError:
        try:
            value = secret[key]
        except KeyError:
            if key == "SECRET_KEY":
                return None
            else:
                error_mssg = (
                    f"Please Setup Environment Variable or Secret JSON for {key}"
                )
                raise ImproperlyConfigured(error_mssg)
        else:
            return value
    else:
        return value


# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = get_var("SECRET_KEY") or "afzal_saiyed"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "account.apps.AccountConfig",
    "rest_framework",
    "corsheaders",
    "api.apps.ApiConfig",
    "cart.apps.CartConfig",
    "blog.apps.BlogConfig",
    "administrator.apps.AdministratorConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "mail_templates"],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]  # Location For static File
MEDIA_ROOT = os.path.join(BASE_DIR, "staticfiles/media/")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/static/")


# CORS SEttings
# # EXPOSE THESE HEADERS
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_REPLACE_HTTPS_REFERER = True


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#      'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny',
#     ]
# }

# Http only cookie with Custom Authentication
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "account.AuthenticationBackend.CustomAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}


AUTH_USER_MODEL = "account.CustomUser"


CART_SESSION_ID = "cart"

# Http Only Cookie for Session and Csrf
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = ["dev.corecare.in", "corecare.in", "development.corecare.in"]
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"


REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
