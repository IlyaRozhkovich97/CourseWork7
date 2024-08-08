from django.conf import settings
import requests
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import logging
import json

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение в Telegram.

    Использует HTTP-запрос к Telegram API для отправки сообщения в указанный чат.

    Аргументы:
        chat_id (str): Идентификатор чата в Telegram, куда будет отправлено сообщение.
        message (str): Текст сообщения, который будет отправлен.

    Логирование:
        - Успешная отправка сообщения: Логируется информационное сообщение.
        - Ошибка при отправке сообщения: Логируется сообщение об ошибке.

    Исключения:
        - Обрабатываются исключения RequestException, возникающие при отправке HTTP-запроса.
    """
    try:
        params = {
            "text": message,
            "chat_id": chat_id,
        }
        response = requests.get(f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage", params=params)
        response.raise_for_status()
        logger.info("Сообщение успешно отправлено.")
    except requests.RequestException as e:
        logger.error(f"Ошибка при отправке сообщения в Telegram: {e}")


def create_periodic_task(username, habit_id, hour, minute, week_list, message, chat_id):
    """
    Создает периодическую задачу для отправки уведомлений.

    Эта функция создает или обновляет периодическую задачу с использованием Django Celery Beat.
    Задача отправляет сообщение в Telegram в соответствии с заданным расписанием.

    Аргументы:
        username (str): Имя пользователя, для которого создается задача.
        habit_id (int): Идентификатор привычки.
        hour (int): Час, в который должна выполняться задача.
        minute (int): Минута, в которую должна выполняться задача.
        week_list (list): Список дней недели, когда должна выполняться задача.
        message (str): Сообщение, которое будет отправлено.
        chat_id (str): Идентификатор чата в Telegram.

    Логирование:
        - Успешное создание или обновление задачи: Логируется информационное сообщение.
        - Ошибка при создании задачи: Логируется сообщение об ошибке.

    Исключения:
        - Обрабатываются исключения, возникающие при создании или обновлении задачи.
    """
    try:

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )

        periodic_task, created = PeriodicTask.objects.get_or_create(
            name=f"habit_{habit_id}_{username}",
            task="send_information_about_habit",
            interval=schedule,
            kwargs=json.dumps({
                "message": message,
                "tg_chat_id": chat_id
            }),
        )

        if created:
            periodic_task.expires = datetime.utcnow() + timedelta(seconds=30)
            periodic_task.save()
            logger.info(f"Создана периодическая задача: {periodic_task}")
        else:
            logger.info(f"Задача уже существует: {periodic_task}")

    except Exception as e:
        logger.error(f"Ошибка при создании периодической задачи: {e}")


def disable_periodic_task(username, habit_id):
    """
    Отключает периодическую задачу.

    Эта функция деактивирует задачу, созданную для определенной привычки и пользователя.

    Аргументы:
        username (str): Имя пользователя, для которого создана задача.
        habit_id (int): Идентификатор привычки.

    Логирование:
        - Успешное отключение задачи: Логируется информационное сообщение.
        - Задача не найдена: Логируется предупреждающее сообщение.
        - Ошибка при отключении задачи: Логируется сообщение об ошибке.

    Исключения:
        - Обрабатываются исключения DoesNotExist и другие возможные ошибки.
    """
    try:
        task = PeriodicTask.objects.get(name=f"habit_{habit_id}_{username}")
        task.enabled = False
        task.save()
        logger.info(f"Задача отключена: {task}")
    except PeriodicTask.DoesNotExist:
        logger.warning(f"Задача не найдена для отключения: habit_{habit_id}_{username}")
    except Exception as e:
        logger.error(f"Ошибка при отключении задачи: {e}")
