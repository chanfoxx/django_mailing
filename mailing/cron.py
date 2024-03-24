from datetime import timedelta

from django.utils import timezone

from mailing.models import Mailing
from mailing.services import mailing_send


def change_status_launched() -> None:
    """ Меняет статус рассылки в состояние - запущено. """
    current_datetime = timezone.now()
    # Выбирает все рассылки, которые удовлетворяют фильтрам:
    # статус - "Создано", текущее время в границах установленного.
    mailing = Mailing.objects.filter(status='CR',
                                     start_time__lte=current_datetime,
                                     end_time__gte=current_datetime)
    for mail in mailing:
        mail.status = 'LC'  # Меняет статус на "Запущено".
        mail.save()


def mailing_in_frequency() -> None:
    """ Работает с рассылками(отправляет письма) разной периодичности. """
    current_datetime = timezone.now()
    # Выбирает все рассылки, которые удовлетворяют фильтру: статус - "Запущено".
    mailing = Mailing.objects.filter(status='LC')

    for mail in mailing:
        # Проверяет наличие логов.
        if mail.logs.exists():
            # Если логи есть:
            # Вычисляет разницу во времени от последнего лога.
            date_diff = current_datetime - mail.logs.last().date
            # Проверяет, прошел ли день/неделя/месяц с последней рассылки.
            # Если да, отправляет рассылку; в ином случае ничего не делает.
            if date_diff >= timedelta(days=1) and mail.frequency == '1/1':
                mailing_send(mail)
            elif date_diff >= timedelta(days=7) and mail.frequency == '1/7':
                mailing_send(mail)
            elif date_diff >= timedelta(days=30) and mail.frequency == '1/30':
                mailing_send(mail)
            else:
                pass
        else:
            # Если логов еще нет - просто отправляет рассылку.
            mailing_send(mail)


def change_status_completed() -> None:
    """ Меняет статус рассылки в состояние - завершено. """
    current_datetime = timezone.now()
    mailing = Mailing.objects.filter(status='LC',
                                     end_time__lte=current_datetime)

    for mail in mailing:
        mail.status = 'CL'  # Меняет статус на "Завершено".
        mail.save()


def main_job() -> None:
    """ Задачи для выполнения cron'ом. """
    change_status_launched()
    mailing_in_frequency()
    change_status_completed()
