from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy
from pytils.translit import slugify
from blog.forms import BlogForm
from blog.models import Blog
from django.views.generic import (ListView, DetailView, DeleteView,
                                  CreateView, UpdateView)
from mailing.models import Mailing, Client


def is_contentmanager(user):
    """Возвращает булево значение на вхождение пользователя в группу."""
    return user.groups.filter(name='Контент-менеджер').exists()


class MainListView(ListView):
    """Контроллер для отображения главной страницы."""
    model = Blog  # Модель для контроллера.
    template_name = 'blog/main.html'  # Шаблон главной страницы.
    extra_context = {'title': 'YourMailing'}  # Название главной страницы.

    def get_queryset(self):
        """Возвращает 6 опубликованных товаров."""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)[:2]

        return queryset

    def get_context_data(self, *args, **kwargs):
        """Получает контекстные данных для страницы."""
        context_data = super().get_context_data(*args, **kwargs)
        context_data['mailing_count'] = Mailing.objects.all().count()
        context_data['mailing_active'] = Mailing.objects.filter(status='LC').count()
        context_data['mailing_client'] = Client.objects.all().count()

        return context_data


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания блоговой записи."""
    model = Blog  # Модель для контроллера.
    form_class = BlogForm  # Форма для контроллера.
    permission_required = ('blog.add_blog',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('blog:blog_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        user = self.request.user
        # Проверяем, является ли пользователь контент-менеджером.
        return is_contentmanager(user) or user.is_superuser

    def form_valid(self, form):
        """Проверяет валидность формы, если успешно - сохраняет ее."""
        if form.is_valid():
            new_blog = form.save()
            new_blog.creator = self.request.user
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения блога."""
    model = Blog  # Модель для контроллера.
    extra_context = {'title': 'Наш блог'}  # Название страницы.

    def get_queryset(self, *args, **kwargs):
        """Возвращает опубликованные записи."""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True).order_by('creation_date').reverse()

        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения определенной записи."""
    model = Blog  # Модель для контроллера.

    def get_object(self, queryset=None):
        """Счетчик просмотров записи."""
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()

        return self.object


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для изменения определенной блоговой записи."""
    model = Blog  # Модель для контроллера.
    form_class = BlogForm  # Форма для контроллера.
    permission_required = ('blog.update_blog',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('blog:blog_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        user = self.request.user
        # Проверяем, является ли пользователь контент-менеджером.
        return is_contentmanager(user) or user.is_superuser

    def form_valid(self, form):
        """Проверяет валидность формы, если успешно - сохраняет ее."""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс для удаления определенной блоговой записи."""
    model = Blog  # Модель для контроллера.
    permission_required = ('blog.delete_blog',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('blog:blog_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        user = self.request.user
        # Проверяем, является ли пользователь контент-менеджером.
        return is_contentmanager(user) or user.is_superuser
