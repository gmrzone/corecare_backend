from .base import *
from datetime import timedelta
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    
    # Http Only Cookie
    'AUTH_COOKIE': 'access_token',  # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_REFRESH': 'refresh_token',  # refresh Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_DOMAIN': None,     # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_SECURE': True,    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_HTTP_ONLY' : True, # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Whether to set the flag restricting cookie leaks on cross-site requests.
                                    # This can be 'Lax', 'Strict', or None to disable the flag.
}


sentry_sdk.init(
    dsn="https://75ecc79fbbdf4351a9a046aa59e82fe4@o622317.ingest.sentry.io/5752665",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_var("PG_PROD_DB_NAME"),
        'USER': get_var("PG_PROD_DB_USER"),
        'PASSWORD': get_var("PG_PROD_DB_PASSWORD"),
        'HOST': get_var("PG_PROD_DB_HOST"),
        'PORT': '5432',
    }
}
ADMINS = (('Afzal', 'saiyedafzalgz@gmail.com'), ('afzal1', 'saiyedafzalaz@gmail.com'), ('Samar', 'dalvisamar333@gmail.com'))


# # # HTTPS Settings
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

# # # HSTS SETTINGS
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': get_var("REDIS_LOCATION_AUTH"),	
        'TIMEOUT': 10800
    },
}


REDIS_HOST = get_var("REDIS_HOST")
REDIS_PORT = int(get_var("REDIS_PORT"))
REDIS_DB = int(get_var("REDIS_DB"))   
REDIS_PASSWORD = get_var("REDIS_PASSWORD")

CELERY_BROKER_URL = get_var("REDIS_LOCATION_AUTH")


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_var("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_var("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER