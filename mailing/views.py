from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic import (ListView, CreateView, DetailView, UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from mailing.forms import MailingForm, MessageForm, ClientForm, ManagerForm
from mailing.models import Mailing, Message, Client, Logs


def is_manager(user):
    """Возвращает булево значение на вхождение пользователя в группу."""
    return user.groups.filter(name='Менеджер').exists()


# Mailing


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения всех рассылок."""
    model = Mailing  # Модель для контроллера.

    def get_queryset(self):
        """
        Возвращает список рассылок по номеру категории и
        статусу публикации для отображения на странице.
        """
        queryset = super().get_queryset()  # Переопределяем метод.
        queryset = queryset.filter(status__in=('CR', 'LC'))

        return queryset


class MailingEndingListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения всех рассылок."""
    model = Mailing  # Модель для контроллера.
    # Шаблон страницы завершенных рассылок.
    template_name = 'mailing/mailing_list_complete.html'

    def get_queryset(self):
        """
        Возвращает список товаров по номеру категории и
        статусу публикации для отображения на странице.
        """
        queryset = super().get_queryset()  # Переопределяем метод.
        queryset = queryset.filter(status='CL')

        return queryset


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания новой рассылки."""
    model = Mailing  # Модель для контроллера.
    form_class = MailingForm  # Форма для контроллера.
    permission_required = ('mailing.add_mailing',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        user = self.request.user
        # Проверяем, имеет ли пользователь необходимые права.
        return user.has_perms(perms)

    def form_valid(self, form):
        """Валидация формы создания товара и версий."""
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.creator = self.request.user
            new_mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для изменения определенной рассылки."""
    model = Mailing  # Модель для контроллера.
    form_class = MailingForm  # Форма для контроллера.
    permission_required = ('mailing.set_status',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        # Получаем объект товара и текущего пользователя.
        mailing = self.get_object()
        user = self.request.user
        # Проверяем, является ли пользователь владельцем товара,
        # либо имеет необходимые права.
        return user == mailing.creator or user.has_perms(perms)

    def get_form_class(self):
        """Возвращает форму в зависимости от роли пользователя."""
        user = self.request.user
        mailing = self.get_object()

        if is_manager(user):
            return ManagerForm
        elif user.is_superuser or user == mailing.creator:
            return MailingForm


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс для отображения определенной рассылки."""
    model = Mailing  # Модель для контроллера.
    permission_required = ('mailing.view_mailing',)  # Разрешения.

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        # Получаем объект рассылки и текущего пользователя.
        mailing = self.get_object()
        user = self.request.user
        # Проверяем, является ли пользователь автором рассылки,
        # либо имеет необходимые права.
        return user == mailing.creator or user.has_perms(perms)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс для удаления определенной рассылки."""
    model = Mailing  # Модель для контроллера.
    permission_required = ('mailing.delete_mailing',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        # Получаем объект рассылки и текущего пользователя.
        mailing = self.get_object()
        user = self.request.user
        # Проверяем, является ли пользователь автором рассылки,
        # либо имеет необходимые права.
        return user == mailing.creator or user.has_perms(perms)


# MailingMessage


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс для создания нового сообщения."""
    model = Message  # Модель для контроллера.
    form_class = MessageForm  # Форма для контроллера.
    permission_required = ('mailing.add_message',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('mailing:mailing_create')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        user = self.request.user
        # Проверяем, имеет ли пользователь необходимые права.
        return not is_manager(user)


# Client


class ClientListView(LoginRequiredMixin, ListView):
    """Класс для отображения всех рассылок."""
    model = Client  # Модель для контроллера.


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс для создания нового получателя."""
    model = Client  # Модель для контроллера.
    form_class = ClientForm  # Форма для контроллера.
    permission_required = ('mailing.add_client',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('mailing:mailing_create')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        user = self.request.user
        # Проверяем, имеет ли пользователь необходимые права.
        return not is_manager(user)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс для удаления определенной рассылки."""
    model = Client  # Модель для контроллера.
    permission_required = ('mailing.delete_client',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        # Получаем объект клиента и текущего пользователя.
        client = self.get_object()
        user = self.request.user
        # Проверяем, является ли пользователь создателем объекта клиента,
        # либо имеет необходимые права.
        return user == client.creator or user.has_perms(perms)
