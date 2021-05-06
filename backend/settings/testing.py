from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# POSTGRESS DEVELOPMENT
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ["PG_DEV_DB_NAME"],
#         'USER': os.environ["PG_DEV_DB_USER"],
#         'PASSWORD': os.environ["PG_DEV_DB_PASSWORD"],
#         'HOST': os.environ["PG_DEV_DB_HOST"],
#         'PORT': '5432',
#     }
# }
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