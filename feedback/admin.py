"""Модуль для работы с административной панелью."""
from django.contrib import admin
from feedback.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Отображение контактных данных в административной панели."""
    list_display = ('id', 'name', 'phone', 'email', 'message',)
