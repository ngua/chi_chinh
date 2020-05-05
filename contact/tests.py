from django.test import TestCase
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django_dramatiq.test import DramatiqTestCase
from .models import Contact
from .tasks import mail_admins_task


class ContactViewTestCase(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(
            response.status_code,
            200
        )


class ContactViewAPITestCase(APITestCase):
    def setUp(self):
        self.test_data = {
            'name': 'Test',
            'email': 'test@test.com',
            'message': 'Test',
            'phone': ''
        }

    def test_successful_post(self):
        response = self.client.post(
            reverse('contact-endpoint'),
            self.test_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_response_data(self):
        response = self.client.post(
            reverse('contact-endpoint'),
            self.test_data,
            format='json'
        )
        self.assertTrue(
            all(
                item in response.data.values() for
                item in self.test_data.values() if item
            )
        )

    def test_model_creation(self):
        self.client.post(
            reverse('contact-endpoint'),
            self.test_data,
            format='json'
        )
        self.assertTrue(Contact.objects.exists())
        contact = Contact.objects.first()
        self.assertTrue(
            contact.name == self.test_data['name'],
            contact.email == self.test_data['email']
        )

    def test_honeypot(self):
        spurious_data = {k: v for k, v in self.test_data.items()}
        spurious_data['phone'] = '10203920'
        response = self.client.post(
            reverse('contact-endpoint'),
            spurious_data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class EmailTaskTestCase(DramatiqTestCase):
    def setUp(self):
        self.test_data = {
            'name': 'Test',
            'email': 'test@test.com',
            'message': 'Test',
            'phone': ''
        }
        self.client = APIClient()

    def test_email_task(self):
        mail_admins_task.send(
            subject='Test',
            message='Test'
        )
        self.broker.join('default')
        self.worker.join()
        self.assertEqual(
            len(mail.outbox),
            1
        )

    def test_email_after_post(self):
        self.client.post(
            reverse('contact-endpoint'),
            self.test_data,
            format='json'
        )
        self.broker.join('default')
        self.worker.join()
        self.assertEqual(
            len(mail.outbox),
            1
        )
        self.assertEqual(
            mail.outbox[0].body,
            self.test_data['message']
        )
