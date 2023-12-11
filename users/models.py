from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя."""
    username = None
    email = models.EmailField(unique=True, verbose_name='E-mail')
    avatar = models.ImageField(upload_to='images/users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(max_length=150, verbose_name='Страна', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Аккаунт активен', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        permissions = [
            ('set_is_active', 'Может блокировать пользователей сервиса'),
        ]


class EmailVerification(models.Model):
    """Модель верификации почты."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    token = models.CharField(max_length=64, verbose_name='Токен', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Токен активен', **NULLABLE)

    def __str__(self) -> str:
        """Возвращает строковое представление о классе верификации почты."""
        return f'{self.user}: "{self.token}"'

    class Meta:
        """Метаданные для модели верификации почты."""
        verbose_name = 'Токен для почты'
        verbose_name_plural = 'Токены для почты'
