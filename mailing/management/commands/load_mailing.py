from django.core.management.base import BaseCommand
from config.settings import MAILING_FILE
import json

from mailing.models import Mailing, Message
from users.models import User


class Command(BaseCommand):
    """ Загружает данные из фикстуры в таблицу БД рассылок. """

    def handle(self, *args, **kwargs):
        with open(MAILING_FILE, encoding='utf-8') as file:
            data = json.load(file)
            for mailing in data:
                message = Message.objects.get(id=mailing['fields']['message'])
                creator = User.objects.get(id=mailing['fields']['creator'])
                clients_ids = mailing['fields']['clients']

                new_mailing = Mailing.objects.create(
                    start_time=mailing['fields']['start_time'],
                    end_time=mailing['fields']['end_time'],
                    message=message,
                    frequency=mailing['fields']['frequency'],
                    status=mailing['fields']['status'],
                    creator=creator,
                )

                for client_id in clients_ids:
                    new_mailing.clients.create(id=client_id)
