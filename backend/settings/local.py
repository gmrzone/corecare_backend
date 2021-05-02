from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

INSTALLED_APPS.append('debug_toolbar')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': "redis://127.0.0.1:6379/1",
        'TIMEOUT': 600
    },
}

SECURE_SSL_REDIRECT = False

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]