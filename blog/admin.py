"""Модуль для работы с административной панелью."""
from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Отображение блоговых записей в административной панели."""
    list_display = ('id', 'title', 'creation_date', 'view_count',)
    list_filter = ('creation_date', 'view_count',)
