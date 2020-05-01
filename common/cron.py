from time import sleep
from threading import Thread
from django.db import connection
from apscheduler.schedulers.background import BackgroundScheduler
from .models import CronJob


scheduler = BackgroundScheduler()


def wait_for_db(table_name, retries=10):
    for _ in range(retries):
        tables = connection.introspection.table_names()
        if table_name not in tables:
            sleep(1)
            continue
        return


def cron(crontab):
    t = Thread(target=wait_for_db, args=('common_cronjob',))
    t.start()
    t.join()

    def inner(actor):
        CronJob.objects.update_or_create(**{
            'module': actor.fn.__module__,
            'name': actor.fn.__name__,
            'crontab': crontab
        })
        return actor

    return inner


def start():
    for cronjob in CronJob.objects.all():
        cronjob.schedule_job(scheduler)
    scheduler.start()
