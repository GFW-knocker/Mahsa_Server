from .base import *

REDIS_HOST = "redis"
XRAY_HOST = "xray"

DEBUG = False

ALLOWED_HOSTS = ["localhost", "*"]

CORS_ALLOWED_ORIGINS = [
    os.environ.get('WEBSITE_URL', 'http://localhost')
]
CSRF_TRUSTED_ORIGINS = [
    os.environ.get('WEBSITE_URL', 'http://localhost'),
    'http://localhost'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../shared/db.sqlite3',
    }
}