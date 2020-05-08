"""
WSGI config for chi_chinh project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from common import scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()

# The apscheduler instance in the `scheduler` module must be called here, before
# dramatiq forks and creates 8 duplicate schedulers

scheduler.start()
