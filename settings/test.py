from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DRAMATIQ_BROKER={
    "BROKER": "dramatiq.brokers.stub.StubBroker",
    "OPTIONS": {},
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Pipelines",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ]
}

CACHE_TTL = 10
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# To test custom `get_settings` templatetag
TEST_STRING = 'Test'
SETTINGS_EXPORT = ('TEST_STRING',)
