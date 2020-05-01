from django.db import models
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPage
from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget
from .models import CronJob


admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class FlatPageAdmin(TranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }


@admin.register(CronJob)
class CronJobAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'crontab', 'next_scheduled')
