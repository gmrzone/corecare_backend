from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    
    # Http Only Cookie
    'AUTH_COOKIE': 'access_token',  # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_REFRESH': 'refresh_token',  # refresh Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_DOMAIN': None,     # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_SECURE': False,    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_HTTP_ONLY' : True, # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Whether to set the flag restricting cookie leaks on cross-site requests.
                                    # This can be 'Lax', 'Strict', or None to disable the flag.
}

CSRF_TRUSTED_ORIGINS = ["127.0.0.1"]

# POSTGRES Development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_var("PG_DEV_DB_NAME"),
        'USER': get_var("PG_DEV_DB_USER"),
        'PASSWORD': get_var("PG_DEV_DB_PASSWORD"),
        'HOST': get_var("PG_DEV_DB_HOST"),
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': "redis://127.0.0.1:6379/1",
        'TIMEOUT': 600
    },
}
SECURE_SSL_REDIRECT = False

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1