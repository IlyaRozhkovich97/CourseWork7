from celery import shared_task
from telegram import Bot
from django.conf import settings
import asyncio
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение в Telegram с использованием бота.
    """
    bot_token = settings.TELEGRAM_TOKEN
    bot = Bot(token=bot_token)

    async def async_send_message():
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            logger.info(f"Сообщение отправлено в Telegram. Chat ID: {chat_id}, Message: {message}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в Telegram: {e}")

    asyncio.run(async_send_message())
