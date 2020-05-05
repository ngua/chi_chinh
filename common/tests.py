from unittest.mock import MagicMock
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase, SimpleTestCase
from django.template import Template, Context
from django_dramatiq.test import DramatiqTestCase
from dramatiq import actor
from .cron import cron
from .models import CronJob


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class CreateCronJobTest(DramatiqTestCase):
    def setUp(self):
        self.func = MagicMock()
        self.func.__name__ = 'func'
        self.func.queue_name = 'func'
        self.actor = actor(self.func)
        cron('* * * * *')(self.actor)
        self.cron_job = CronJob.objects.first()

    def test_cron_creation(self):
        self.assertTrue(CronJob.objects.exists())
        self.assertEqual(self.cron_job.name, 'func')

    def test_cron_schedule(self):
        self.cron_job = CronJob.objects.first()
        self.assertTrue(
            self.cron_job.next_scheduled > timezone.now()
        )
        self.assertTrue(
            self.cron_job.next_scheduled - timezone.now() <
            timedelta(minutes=1)
        )


class TemplateTagsTestCase(TestCase):
    def test_settings_attr_tag(self):
        template = Template(
            '{% load chi_chinh_extras %} {% get_setting "TEST_STRING" %}'
        )
        rendered = template.render(Context({}))
        self.assertInHTML(
            'Test',
            rendered
        )

    def test_settings_raise(self):
        template = Template(
            '{% load chi_chinh_extras %} {% get_setting "SECRET_KEY" %}'
        )
        with self.assertRaises(AttributeError):
            template.render(Context({}))


class ErrorHandlerTestCase(SimpleTestCase):
    def test_404_handler_render(self):
        response = self.client.get('/does_not_exist/')
        self.assertContains(
            response,
            'Chị Chinh'
        )
