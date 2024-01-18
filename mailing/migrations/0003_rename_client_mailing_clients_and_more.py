# Generated by Django 4.2.7 on 2023-12-27 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_mailing_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailing',
            old_name='client',
            new_name='clients',
        ),
        migrations.AlterField(
            model_name='logs',
            name='mailing_settings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='mailing.mailing', verbose_name='Настройки'),
        ),
    ]