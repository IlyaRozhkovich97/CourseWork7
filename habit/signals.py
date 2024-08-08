from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Habits
from .tasks import send_telegram_message
from django.conf import settings


@receiver(post_save, sender=Habits)
def notify_telegram_on_new_habit(sender, instance, created, **kwargs):
    """
    Отправляет уведомление в Telegram при создании новой привычки.

    Этот сигнал срабатывает после сохранения новой привычки в базе данных.
    Если привычка была создана (а не обновлена), то отправляется сообщение в Telegram с информацией о новой привычке.

    Аргументы:
        sender (Model): Модель, которая инициировала сигнал.
        instance (Habits): Экземпляр модели Habits, который был сохранен.
        created (bool): Флаг, указывающий, была ли привычка создана (True) или обновлена (False).
        **kwargs: Дополнительные аргументы.

    Действия:
        - Формирует сообщение с информацией о новой привычке.
        - Использует задачу Celery для отправки сообщения в Telegram по заданному chat_id.
    """
    if created:
        chat_id = settings.TELEGRAM_CHAT_ID
        message = (
            f"Новая привычка создана:\n"
            f"Место: {instance.place}\n"
            f"Время: {instance.time}\n"
            f"Действие: {instance.action}\n"
            f"Периодичность: {instance.periodicity} день(ей)\n"
            f"Длительность: {instance.duration} секунд\n"
        )
        send_telegram_message.delay(chat_id, message)
