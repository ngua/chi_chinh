import dramatiq
from django.contrib.sitemaps import ping_google
from django_dramatiq.tasks import delete_old_tasks
from .cron import cron


@cron('0 0 * * 6')
@dramatiq.actor
def clean_task_db():
    """
    Calls django_dramatiq delete_old_tasks method once weekly to clear db of
    dramatiq actors older than one week
    """
    delete_old_tasks(max_task_age=604800)


@cron('0 0 * * 6')
@dramatiq.actor(max_retries=4)
def ping():
    """
    Schedules weekly google ping
    """
    try:
        ping_google(sitemap_url='/sitemap.xml')
    except Exception:
        pass
