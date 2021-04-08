from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# POSTGRESS PRODUCTION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'corecare',
        'USER': 'afzal',
        'PASSWORD': '27021992samgalnote4',
        'HOST': '172.105.54.166',
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
        'LOCATION': 'redis://:27021992samgalnote4@127.0.0.1:6379/1',	
        'TIMEOUT': 600
    },
}
