import dramatiq
from django.core.mail import mail_admins


@dramatiq.actor
def mail_admins_task(subject, message):
    """
    Calls Django mail_admins from dramatiq actor.

    :param str subject: from Contact serializer
    :param str message: from Contact serializer
    """
    mail_admins_task.logger.info('Contact email sent to admins')
    mail_admins(subject, message)
