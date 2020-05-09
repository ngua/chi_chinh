from .base import *

DEBUG = True

# Cache settings

CACHE_TTL = 10
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
