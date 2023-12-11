from django.db import models
from django.conf import settings


NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """Модель блоговой записи."""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='Slug', **NULLABLE)
    description = models.TextField(verbose_name='Содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='images/blog/',
                                verbose_name='Изображение',
                                **NULLABLE)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    view_count = models.IntegerField(default=0, verbose_name='Просмотры')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                **NULLABLE, verbose_name='Автор')

    def __str__(self):
        """Возвращает строковое представление о классе блоговой записи."""
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
