import sentry_sdk
import os
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *

DEBUG = False

# Static/media files

DEFAULT_FILE_STORAGE = 'storage.SpacesMediaStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIAFILES_LOCATION = 'media'

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

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'storage.SpacesStaticStorage'
STATIC_URL = f'{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
STATIC_URL = f'{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

# Redi

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
    }
}

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

# sentry_sdk.init(
#     dsn=os.environ.get('SENTRY_DSN'),
#     integrations=[DjangoIntegration()],
#     send_default_pii=True
# )
