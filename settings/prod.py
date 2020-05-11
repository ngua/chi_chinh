import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'jet',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',
    'django.contrib.staticfiles',
    'storages',
    'django.contrib.postgres',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'ckeditor',
    'rest_framework',
    'django_filters',
    'django_dramatiq',
    'django_bleach',
    'common.apps.CommonConfig',
    'search.apps.SearchConfig',
    'recipes.apps.RecipesConfig',
    'contact.apps.ContactConfig'
]

# Static/media files

DEFAULT_FILE_STORAGE = 'storage.SpacesMediaStorage'
STATICFILES_STORAGE = 'storage.SpacesStaticStorage'
PATH_PREFIX = 'chi_chinh'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_LOCATION = f'{PATH_PREFIX}/static'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIAFILES_LOCATION = f'{PATH_PREFIX}/media'

AWS_ACCESS_KEY_ID = os.environ.get('SPACES_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('SPACES_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('SPACES_BUCKET')
AWS_S3_ENDPOINT_URL = os.environ.get('SPACES_ENDPOINT')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('SPACES_EDGE')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = 'public-read'

# Redis

REDIS_URI = os.environ.get('REDIS_URI')

# Cache settings

CACHE_TTL = 60 * 15
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URI,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'chichinh_'
    },
    'collectfast': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'collectfast_cache',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 10000
        }
    }
}

# Collectfast

COLLECTFAST_STRATEGY = 'collectfast.strategies.boto3.Boto3Strategy'
COLLECTFAST_CACHE = 'collectfast'
COLLECTFAST_THREADS = 10

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

# Sentry
ignore_errors = [KeyboardInterrupt]
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
    ignore_errors=ignore_errors
)
