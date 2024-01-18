from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings

from mailing.models import Logs


def mailing_send(mail):
    """ Формирует и отправляет письмо на e-mail пользователя/пользователей. """
    try:
        # Пробует отправить сообщение.
        send_mail(
            subject=mail.message.subject,
            message=mail.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=mail.clients.values_list('email', flat=True),
            fail_silently=False,
        )
    except SMTPException(OSError) as e:
        # Если возникает ошибка почтового сервиса записывает логи с ошибкой:
        Logs.objects.create(attempt_status=2,
                            mail_server_response=str(e),
                            mailing_settings=mail)
    except Exception as e:
        # Записывает логи если возникла другая ошибка.
        Logs.objects.create(attempt_status=2,
                            mail_server_response=str(e),
                            mailing_settings=mail)
    else:
        # Записывает успешные логи.
        Logs.objects.create(attempt_status=1,
                            mail_server_response='OK',
                            mailing_settings=mail)
