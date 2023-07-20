from .base import *

REDIS_HOST = "redis"
XRAY_HOST = "xray"

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../shared/db.sqlite3',
    }
}