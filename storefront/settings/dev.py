from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-1*#@anw%s96@*@x&i&m#lo_lqey1ef)^r9_9y^fc5e(^ja7$k4'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'storefront',  
        'USER': 'root',  
        'PASSWORD': 'youssef1992002',  
        'HOST': '127.0.0.1',  
        'PORT': '3306',  
    }  
}  


CELERY_BROKER_URL = 'redis://localhost:6379/1'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",# the number 2 indecate the second data base the 1 is inuse as a messagebroker database
        "TIMEOUT": 10*60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT = 2525