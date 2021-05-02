from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# POSTGRESS PRODUCTION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["PG_PROD_DB_NAME"],
        'USER': os.environ["PG_PROD_DB_USER"],
        'PASSWORD': os.environ["PG_PROD_DB_PASSWORD"],
        'HOST': os.environ["PG_PROD_DB_HOST"],
        'PORT': '5432',
    }
}

ADMINS = (('Afzal', 'saiyedafzalgz@gmail.com'), ('afzal1', 'saiyedafzalaz@gmail.com'), ('Samar', 'dalvisamar333@gmail.com'))


# # HTTPS Settings
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

# # HSTS SETTINGS
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': os.environ["REDIS_LOCATION_AUTH"],	
        'TIMEOUT': 600
    },
}
