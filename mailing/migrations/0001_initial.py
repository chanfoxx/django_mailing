# Generated by Django 4.2.7 on 2023-12-09 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, verbose_name='Контактный e-mail')),
                ('full_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='ФИО')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('creator', models.ForeignKey(blank=True, default=53, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Клиент сервиса',
                'verbose_name_plural': 'Клиенты сервиса',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=150, null=True, verbose_name='Тема письма')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Тело письма')),
            ],
            options={
                'verbose_name': 'Сообщение рассылки',
                'verbose_name_plural': 'Сообщения рассылок',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Время начала рассылки')),
                ('end_time', models.DateTimeField(verbose_name='Время окончания рассылки')),
                ('frequency', models.CharField(choices=[('1/1', 'Раз в день'), ('1/7', 'Раз в неделю'), ('1/30', 'Раз в месяц')], default='1/1', max_length=4, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('CL', 'Завершено'), ('LC', 'Запущено'), ('CR', 'Создано')], default='CR', max_length=2, verbose_name='Статус рассылки')),
                ('client', models.ManyToManyField(to='mailing.client', verbose_name='Получатель')),
                ('creator', models.ForeignKey(blank=True, default=53, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Продавец')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='Контент')),
            ],
            options={
                'verbose_name': 'Настройки рассылки.',
                'verbose_name_plural': 'Настройки рассылок',
                'permissions': [('set_status', 'Может отключать рассылки')],
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата и время последней попытки')),
                ('attempt_status', models.IntegerField(blank=True, choices=[(1, 'Успешно'), (2, 'Неудачно')], null=True, verbose_name='Статус попытки')),
                ('mail_server_response', models.CharField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.client', verbose_name='Получатель')),
                ('mailing_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Настройки')),
            ],
            options={
                'verbose_name': 'Логи рассылки',
                'verbose_name_plural': 'Логи рассылок',
            },
        ),
    ]
