from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .tokens import account_activation_token
from .models import Customer


logger = get_task_logger(__name__)


@shared_task(name="send_activation_email_task")
def send_activate_email_task(domain, is_secure, user_id, to_email):
    """Sends confirmation email. If not send successfuly, returns False, else -- True."""

    logger.info(f"Sent activation email to {user_id}")

    user = Customer.objects.get(id=user_id)

    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if is_secure else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    return email.send()