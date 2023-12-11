from django import forms
from mailing.models import Mailing, Client, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('status', 'creator',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_time'].widget.attrs.update({'placeholder': 'Пример ввода: 2023-01-01 10:00'})
        self.fields['end_time'].widget.attrs.update({'placeholder': 'Пример ввода: 2023-01-01 11:00'})


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('creator',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class ManagerForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('status',)
