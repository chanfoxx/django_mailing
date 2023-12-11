from django.db import models


class Feedback(models.Model):
    """Модель обратной связи."""
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    email = models.EmailField(max_length=100, verbose_name='E-mail')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self) -> str:
        """Возвращает строковое представление о классе обратной связи."""
        return f'{self.name} (phone: {self.phone})'

    class Meta:
        """Метаданные для модели обратной связи."""
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
