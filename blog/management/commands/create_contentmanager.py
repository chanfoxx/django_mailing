from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from blog.models import Blog


class Command(BaseCommand):
    """Создает группу и добавляет права доступа."""
    def handle(self, *args, **kwargs):
        try:
            new_group = Group.objects.create(name='Контент-менеджер')
            permissions = Permission.objects.filter(content_type__model='blog')
            new_group.permissions.set(permissions)
            new_group.save()
        except Exception as e:
            print(f'Не удалось создать группу.\nОшибка: {str(e)}')
