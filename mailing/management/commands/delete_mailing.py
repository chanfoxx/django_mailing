from django.core.management.base import BaseCommand
from mailing.models import MailingSettings


class Command(BaseCommand):
    """Удаляет данные из таблицы категорий."""
    def handle(self, *args, **kwargs) -> None:
        try:
            MailingSettings.objects.all().delete()
        except Exception as e:
            print(f'Не удалось удалить данные из таблицы категорий.'
                  f'Ошибка: {str(e)}.')
