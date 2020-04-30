"""
WSGI config for chi_chinh project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from common import cron

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()

# The apscheduler instance in the `cron` module must be called here, before
# dramatiq forks into 8 separate processes and creates 8 duplicate schedulers

cron.start()
