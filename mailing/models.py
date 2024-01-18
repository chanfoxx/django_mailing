from django.db import models
from django.conf import settings


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """ Модель клиента сервиса. """
    email = models.EmailField(max_length=100, verbose_name='Контактный e-mail')
    full_name = models.CharField(max_length=250, verbose_name='ФИО', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        verbose_name='Продавец', default=53, **NULLABLE)

    def __str__(self) -> str:
        """ Возвращает строковое представление о классе клиента сервиса. """
        return f'{self.full_name} ({self.email})'

    class Meta:
        """ Метаданные для модели клиента сервиса. """
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'


class Message(models.Model):
    """ Модель сообщения рассылки. """
    subject = models.CharField(max_length=150, verbose_name='Тема письма',
                               **NULLABLE)
    body = models.TextField(verbose_name='Тело письма', **NULLABLE)

    def __str__(self):
        """ Возвращает строковое представление о классе сообщения рассылки. """
        return f'Тема рассылки: "{self.subject}".'

    class Meta:
        """ Метаданные для модели сообщения рассылки. """
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылок'


class Mailing(models.Model):
    """ Модель настроек рассылки. """

    # Выбор для поля "frequency".
    ONCE_A_DAY = "1/1"
    WEEKLY = "1/7"
    MONTHLY = "1/30"

    FREQUENCY_MAILING = [
        (ONCE_A_DAY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    # Выбор для поля "status".
    COMPLETED = "CL"
    LAUNCHED = "LC"
    CREATED = "CR"
    STATUS_MAILING = [
        (COMPLETED, "Завершено"),
        (LAUNCHED, "Запущено"),
        (CREATED, "Создано"),
    ]

    start_time = models.DateTimeField(verbose_name='Время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки')

    frequency = models.CharField(
        max_length=4, choices=FREQUENCY_MAILING,
        default=ONCE_A_DAY, verbose_name='Периодичность')
    status = models.CharField(
        max_length=2, choices=STATUS_MAILING,
        default=CREATED, verbose_name='Статус рассылки')

    clients = models.ManyToManyField(Client, verbose_name='Получатель')
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name='Контент')

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        verbose_name='Продавец', default=1, **NULLABLE)

    def __str__(self):
        """ Возвращает строковое представление о классе настроек рассылки. """
        return f'{self.start_time}:{self.end_time} - {self.frequency}'

    class Meta:
        """ Метаданные для модели настроек рассылки. """
        verbose_name = 'Настройки рассылки.'
        verbose_name_plural = 'Настройки рассылок'

        permissions = [
            ('set_status', 'Может отключать рассылки'),
        ]


class Logs(models.Model):
    """ Модель логов рассылки. """

    # Выбор для поля "attempt_status".
    SUCCESS = 1
    FAILURE = 2

    ATTEMPT_STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILURE, 'Неудачно'),
    ]

    date = models.DateTimeField(auto_now_add=True,
                                verbose_name='Дата и время последней попытки',
                                **NULLABLE)
    attempt_status = models.IntegerField(choices=ATTEMPT_STATUS_CHOICES,
                                         verbose_name='Статус попытки', **NULLABLE)
    mail_server_response = models.CharField(verbose_name='Ответ почтового сервера',
                                            **NULLABLE)

    mailing_settings = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name='Настройки',
        related_name='logs')

    def __str__(self):
        """ Возвращает строковое представление о классе логов рассылки. """
        return f'{self.date}: {self.attempt_status}, {self.mail_server_response}'

    class Meta:
        """ Метаданные для модели логов рассылки. """
        verbose_name = 'Логи рассылки'
        verbose_name_plural = 'Логи рассылок'
