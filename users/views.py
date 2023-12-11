from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from mailing.views import is_manager
from users.forms import UserRegisterForm, UserProfileForm, ManagerForm
from users.models import User, EmailVerification
from users.services import send_new_password, send_confirm_email


class LoginView(BaseLoginView):
    """Контроллер для входа по e-mail и паролю."""
    template_name = 'users/login.html'  # Шаблон формы авторизации.
    extra_context = {'title': 'Вход'}  # Название страницы.


class LogoutView(BaseLogoutView):
    """Контроллер для выхода из текущего пользователя."""
    pass


class RegisterView(CreateView):
    """Контроллер для регистрации."""
    model = User  # Модель для контроллера.
    form_class = UserRegisterForm  # Форма для контроллера.
    # Страница переадресации.
    success_url = reverse_lazy('users:email_confirm')

    def form_valid(self, form):
        """Валидация формы создания пользователя."""
        new_user = form.save()
        new_user.is_active = False
        new_user.save()

        # Генерируем токен.
        token = get_random_string(length=32)
        # Сохраняем нового пользователя и токен в бд.
        EmailVerification.objects.create(user=new_user, token=token)

        verification_url = reverse("users:email_verify", args=[token])
        # Отправляем ссылку на почту пользователю для подтверждения.
        send_confirm_email(verification_url, new_user)

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования профиля."""
    model = User  # Модель для контроллера.
    permission_required = ('users.set_is_active',)  # Разрешения.
    # Страница переадресации.
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Получает текущего пользователя."""
        return self.request.user

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        user = self.request.user
        # Проверяем, является ли пользователь владельцем аккаунта,
        # либо имеет необходимые права.
        return user == self.get_object() or user.has_perms(perms)

    def get_form_class(self):
        """Возвращает форму в зависимости от роли пользователя."""
        user = self.request.user

        if is_manager(user):
            return ManagerForm
        elif user.is_superuser or user == self.get_object():
            return UserProfileForm


class UserListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка пользователей."""
    model = User  # Модель для контроллера.


@permission_required('users.set_is_active')
def set_active(request, pk):
    """Меняет поле 'is_active' пользователя."""
    # Получаем определенного пользователя по 'pk'.
    user = get_object_or_404(User, pk=pk)
    # Меняем поле.
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return redirect('users:users')


class SendConfirmView(TemplateView):
    """Контроллер для отправки подтверждения."""
    # Шаблон подтверждения e-mail.
    template_name = 'users/email_confirmation.html'
    # Название страницы.
    extra_context = {'title': 'Подтверждение почты'}


class EmailErrorView(TemplateView):
    """Контроллер для страницы с ошибкой."""
    template_name = 'users/error_page.html'  # Шаблон ошибки.
    # Название страницы.
    extra_context = {'title': 'Ошибка подтверждения почты'}


class EmailVerifyView(View):
    """Контроллер для подтвержденного e-mail."""
    def get(self, request, *args, **kwargs):
        # Получаем токен из запроса.
        token = self.kwargs.get('token')
        # Находим нужный токен в бд.
        email_verification = EmailVerification.objects.filter(token=token).first()

        if not email_verification:
            return redirect('users:email_error')

        if not email_verification.is_active:
            return redirect('users:email_error')

        new_user = email_verification.user
        new_user.is_active = True
        new_user.save()
        email_verification.is_active = False
        email_verification.save()

        return redirect('users:login')


class PasswordView(TemplateView):
    """Класс для отображения страницы с восстановлением пароля."""
    # Шаблон восстановления пароля.
    template_name = 'users/reset_password.html'
    extra_context = {'title': 'Восстановление пароля'}  # Название страницы.

    def post(self, request, *args, **kwargs):
        """
        POST метод:
        email - e-mail адрес пользователя,
        """
        email = request.POST.get('email')
        # Генерируем новый пароль.
        new_password = User.objects.make_random_password()
        # Отправляем новый пароль на указанную почту пользователем.
        send_new_password(new_password, email)
        # Получаем нужного пользователя по e-mail и сохраняем новый пароль.
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        return redirect(reverse('users:login'))
