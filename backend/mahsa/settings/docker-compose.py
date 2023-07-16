from .base import *

REDIS_HOST = "redis"

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../shared/db.sqlite3',
    }
}