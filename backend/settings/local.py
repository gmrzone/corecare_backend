from datetime import timedelta

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
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

DEBUG = True


INSTALLED_APPS.append("debug_toolbar")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "TIMEOUT": 300,
    },
}

SECURE_SSL_REDIRECT = False

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_DB = 1
REDIS_PASSWORD = None

CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = get_var("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_var("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
