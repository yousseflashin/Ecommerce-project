import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = []


DATABASES = {  
    'default': dj_database_url.config('')
}  

REDIS_URL=['REDIS_URL']

CELERY_BROKER_URL = REDIS_URL


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 10*60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['SMTP_SERVER']
EMAIL_HOST_USER=os.environ['SMTP_LOGIN']
EMAIL_HOST_PASSWORD=os.environ['SMTP_PASSWORD']
EMAIL_PORT = os.environ['SMTP_PORT']