import dramatiq
from django_dramatiq.tasks import delete_old_tasks
from .cron import cron


@cron('0 0 * * 6')
@dramatiq.actor
def clean_task_db():
    delete_old_tasks(max_task_age=604800)
