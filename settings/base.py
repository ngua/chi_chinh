"""
Django settings for chi_chinh project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'testserver']


# Application definition

INSTALLED_APPS = [
    'jet',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'django.contrib.postgres',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'ckeditor',
    'rest_framework',
    'django_filters',
    'webpack_loader',
    'django_dramatiq',
    'django_bleach',
    'common.apps.CommonConfig',
    'search.apps.SearchConfig',
    'recipes.apps.RecipesConfig',
    'contact.apps.ContactConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chi_chinh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chi_chinh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}




# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('vi', _('Vietnamese'))
)

LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

# Media settings

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
RECIPE_PIC_PATH = 'recipe'


# Email settings

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Redis uri for caching, dramatiq, etc...

# REDIS_URI = 'redis://redis:6379'
REDIS_URI = os.environ.get('REDIS_URI')

# Webpack config for react components

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '/bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'static', 'webpack-stats.json'),
    }
}

# Rest framework settings

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ]
}

# Email settings

EMAIL_SUBJECT_PREFIX = '[Chị Chinh] '
ADMINS = [(os.environ.get('SU_USERNAME'), os.environ.get('SU_EMAIL'))]

# Admin site

ADMIN_SITE_HEADER = 'Chị Chinh'
ADMIN_SITE_TITLE = ADMIN_SITE_HEADER

# Vhost

VIRTUAL_HOST = os.environ.get('VIRTUAL_HOST', '').split(',')[0]

# Settings allowed to be exported to templates

SETTINGS_EXPORT = ('VIRTUAL_HOST',)

# Dramatiq settings

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": REDIS_URI,
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ]
}

DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {
        "url": REDIS_URI,
    },
    "MIDDLEWARE_OPTIONS": {
        "result_ttl": 60000
    }
}

# Ckeditor settings

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'custom',
        'toolbar_custom': [
            ['Styles', 'Format', 'Font', 'FontSize'],
            [
                'Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                'Superscript'
            ],
            ['HorizontalRule', 'Table', '-', 'Link', 'Unlink'],
            ['TextColor', 'BGColor'],
            [
                'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
                'Blockquote', '-', 'JustifyLeft', 'JustifyCenter',
                'JustifyRight', 'JustifyBlock'
            ],
            ['Undo', 'Redo'],
            ['RemoveFormat', 'Source'],
        ]
    }
}

# Bleach settings

BLEACH_ALLOWED_TAGS = [
    'p', 'h1', 'h2', 'h3', 'h4', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'br',
    'hr', 'span', 's', 'u', 'table', 'thead', 'tbody', 'tr', 'td',
    'blockquote', 'a'
]
BLEACH_ALLOWED_ATTRIBUTES = [
    'href', 'title', 'name', 'style', 'border', 'cellpadding', 'cellspacing'
]
BLEACH_ALLOWED_STYLES = [
    'font-family', 'font-weight', 'font-size', 'text-decoration', 'font-variant', 'color',
    'width', 'text-align', 'margin-left'
]
BLEACH_STRIP_TAGS = True
BLEACH_DEFAULT_WIDGET = 'ckeditor.widgets.CKEditorWidget'

# Sites

SITE_ID = 1
