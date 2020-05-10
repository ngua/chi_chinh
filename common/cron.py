from time import sleep
from threading import Thread
from django.db import connection, ProgrammingError
from .models import CronJob


def wait_for_db(table_name, retries=1000):
    """
    Ensures a given db table exists. Intended to be used as a timer in separate
    thread

    :param str table_name: Name of db table to verify, using
        Django's db connection introspection method
    :param int retries: Number of times to retry before function returns,
        with intervening 10s sleep (default 1000)
    :returns NoneType: returns None
    """
    for _ in range(retries):
        tables = connection.introspection.table_names()
        if table_name not in tables:
            sleep(10)
            continue
        return


def cron(crontab):
    """
    Decorator function that takes a crontab argument and returns inner dramatiq
    actor decorator. Crontab is used in enclosing scope to create CronJob model
    instance. Calls wait_for_db with cronjob table argument to avoid db write
    before tables exist

    :param str crontab: Crontab-formatted string
    :returns func inner: Inner agent decorator function
    """
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
