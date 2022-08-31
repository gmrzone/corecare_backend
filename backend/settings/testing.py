from datetime import timedelta

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# This setting will only work with docker

DEBUG = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=4),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # Http Only Cookie
    "AUTH_COOKIE": "access_token",  # Cookie name. Enables cookies if value is set.
    "AUTH_COOKIE_REFRESH": "refresh_token",  # refresh Cookie name. Enables cookies if value is set.
    "AUTH_COOKIE_DOMAIN": None,  # A string like "example.com", or None for standard domain cookie.
    "AUTH_COOKIE_SECURE": False,  # Whether the auth cookies should be secure (https:// only).
    "AUTH_COOKIE_HTTP_ONLY": True,  # Http only cookie flag.It's not fetch by javascript.
    "AUTH_COOKIE_PATH": "/",  # The path of the auth cookie.
    "AUTH_COOKIE_SAMESITE": "Lax",  # Whether to set the flag restricting cookie leaks on cross-site requests.
    # This can be 'Lax', 'Strict', or None to disable the flag.
}


# POSTGRES Development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_var("POSTGRES_DB"),
        "USER": get_var("POSTGRES_USER"),
        "PASSWORD": get_var("POSTGRES_PASSWORD"),
        "HOST": get_var("POSTGRES_DB_HOST"),
        "PORT": get_var("PGPORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": get_var("REDIS_LOCATION_AUTH"),
        "TIMEOUT": 300,
    },
}

SECURE_SSL_REDIRECT = False

REDIS_HOST = get_var("REDIS_HOST")
REDIS_PORT = int(get_var("REDIS_PORT"))
REDIS_DB = int(get_var("REDIS_DB"))

CELERY_BROKER_URL = get_var("REDIS_LOCATION_AUTH")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
