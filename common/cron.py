from apscheduler.schedulers.background import BackgroundScheduler
from threading import Timer
from .models import CronJob


scheduler = BackgroundScheduler()


def cron(crontab):
    def inner(actor):
        CronJob.objects.update_or_create(**{
            'module': actor.fn.__module__,
            'name': actor.fn.__name__,
            'crontab': crontab
        })
        return actor

    return inner


def schedule_jobs():
    for cronjob in CronJob.objects.all():
        cronjob.schedule_job(scheduler)
    scheduler.start()


def start():
    t = Timer(10.0, schedule_jobs)
    t.start()
