import croniter
import datetime
from django.db import models
from django.utils import timezone
from apscheduler.triggers.cron import CronTrigger


class CronJob(models.Model):
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    crontab = models.CharField(max_length=255)

    @property
    def next_scheduled(self):
        now = timezone.now()
        cron = croniter.croniter(self.crontab, now)
        return cron.get_next(datetime.datetime)

    def schedule_job(self, scheduler):
        scheduler.add_job(
            str(self),
            CronTrigger.from_crontab(self.crontab),
            id=self.name,
            replace_existing=True
        )

    def __repr__(self):
        return f"CronJob('{self.name}', '{self.module}', '{self.crontab}')"

    def __str__(self):
        return f'{self.module}:{self.name}.send'
