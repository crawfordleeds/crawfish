import logging
from typing import Union

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def send_mail(
    to_email: Union[list, str],
    template_id: str,
    data: dict = {},
    from_email: str = None,
    esp_extra: dict = None,  # https://anymail.readthedocs.io/en/stable/esps/sendgrid/#esp-extra-support)
):
    """"""

    if isinstance(to_email, str):
        to_email = [to_email]
    logger.info(f"Prepping email(s) to: {to_email} using template_id {template_id}")

    num_sent = 0
    connection = mail.get_connection()
    d = {}
    messages = []
    for t in to_email:
        if settings.APP_ENVIRONMENT not in ("production", "prod"):
            """override data and to_email"""
            logger.info(
                f"Not in production. Replacing to email {t} with {settings.SERVER_EMAIL}"
            )
            d[settings.SERVER_EMAIL] = data.get(t, {})
            to = settings.SERVER_EMAIL
        else:
            d = {}
            d[t] = data.get(t)
            to = t
        message = (
            EmailMessage(to=[to])
            if not from_email
            else EmailMessage(to=[to], from_email=from_email)
        )
        if esp_extra:
            message.esp_extra = esp_extra
        message.template_id = template_id
        message.merge_data = d.copy()
        messages.append(message)

    num_sent = connection.send_messages(messages)
    logger.info(f"Send {num_sent} emails with template id {template_id}")
    connection.close()
    return num_sent
