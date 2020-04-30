from django.contrib import admin
from .models import CronJob


@admin.register(CronJob)
class CronJobAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'next_scheduled')
