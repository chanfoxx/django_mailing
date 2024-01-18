from django.core.management.base import BaseCommand
from mailing.models import Mailing


class Command(BaseCommand):
    """Удаляет данные из таблицы рассылок."""
    def handle(self, *args, **kwargs) -> None:
        try:
            Mailing.objects.all().delete()
        except Exception as e:
            print(f'Не удалось удалить данные из таблицы категорий.'
                  f'Ошибка: {str(e)}.')
