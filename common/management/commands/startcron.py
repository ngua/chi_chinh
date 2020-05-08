from django.core.management.base import BaseCommand, CommandError
from django.db import ProgrammingError
from common.scheduler import scheduler
from common.models import CronJob


class Command(BaseCommand):
    help = 'Schedules cron jobs declared in common.cron'

    def handle(self, *args, **options):
        for cron_job in CronJob.objects.all():
            try:
                cron_job.schedule_job(scheduler)
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully scheduled {cron_job.name} '
                    f'next scheduled to run at {cron_job.next_scheduled}'
                ))
            except ProgrammingError:
                raise CommandError(
                    'Cron table not initialized. '
                    'Did you run the necessary migrations?'
                )
