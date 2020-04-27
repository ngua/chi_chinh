import dramatiq
from django.core.mail import mail_admins


@dramatiq.actor
def mail_admins_task(subject, message):
    mail_admins_task.logger.info('Contact email sent to admins')
    mail_admins(subject, message)
