from time import sleep
from threading import Thread
from django.db import connection, ProgrammingError
from .models import CronJob


def wait_for_db(table_name, retries=1000):
    for _ in range(retries):
        tables = connection.introspection.table_names()
        if table_name not in tables:
            sleep(10)
            continue
        return


def cron(crontab):
    t = Thread(target=wait_for_db, args=('common_cronjob',))
    t.start()
    t.join()

    def inner(actor):
        try:
            CronJob.objects.update_or_create(**{
                'module': actor.fn.__module__,
                'name': actor.fn.__name__,
                'crontab': crontab
            })
        except ProgrammingError:
            pass
        return actor

    return inner
