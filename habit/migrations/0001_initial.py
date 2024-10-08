# Generated by Django 5.0.7 on 2024-08-06 12:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=140, verbose_name='Место')),
                ('time', models.TimeField(verbose_name='Время, когда надо выполнить привычку')),
                ('action', models.CharField(max_length=140, verbose_name='Действие, которое надо сделать')),
                ('is_nice', models.BooleanField(choices=[(True, 'Приятная'), (False, 'Нет')], default=True, verbose_name='Приятная')),
                ('periodicity', models.SmallIntegerField(default=1, verbose_name='Периодичность (в днях) - от 1 до 7')),
                ('prize', models.CharField(blank=True, max_length=100, null=True, verbose_name='Вознаграждение')),
                ('duration', models.SmallIntegerField(verbose_name='Время на выполнение (в минутах)')),
                ('is_public', models.BooleanField(choices=[(True, 'Публичная'), (False, 'Нет')], default=True, verbose_name='Публичная')),
                ('monday', models.BooleanField(default=True, verbose_name='Понедельник')),
                ('tuesday', models.BooleanField(default=True, verbose_name='Вторник')),
                ('wednesday', models.BooleanField(default=True, verbose_name='Среда')),
                ('thursday', models.BooleanField(default=True, verbose_name='Четверг')),
                ('friday', models.BooleanField(default=True, verbose_name='Пятница')),
                ('saturday', models.BooleanField(default=True, verbose_name='Суббота')),
                ('sunday', models.BooleanField(default=True, verbose_name='Воскресенье')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Укажите дату создания', null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Укажите дату изменения', null=True, verbose_name='Дата изменения')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habit.habits', verbose_name='Связанная с другой привычкой')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
                'ordering': ['-id'],
            },
        ),
    ]
