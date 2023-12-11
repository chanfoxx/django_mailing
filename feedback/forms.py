from django import forms
from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    """Форма обратной связи."""
    class Meta:
        model = Feedback
        fields = '__all__'
