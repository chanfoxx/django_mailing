from django.urls import reverse_lazy
from feedback.forms import FeedbackForm
from feedback.models import Feedback
from django.views.generic import TemplateView, CreateView


class FeedbackCreateView(CreateView):
    """
    Контроллер для отображения контактной
    информации и формы обратной связи.
    """
    model = Feedback  # Модель для контроллера.
    form_class = FeedbackForm  # Форма для контроллера.
    extra_context = {'title': 'Контакты'}  # Название страницы.
    # Страница переадресации.
    success_url = reverse_lazy('feedback:feedback_thanks')


class FeedbackThankView(TemplateView):
    """Класс для подтверждения обратной связи."""
    template_name = 'feedback/feedback_gratitude.html'  # Название шаблона.
    extra_context = {'title': 'Обратная связь'}  # Название страницы.
