from django.core.management.base import BaseCommand
from telegram import Bot
from django.conf import settings
import asyncio


class Command(BaseCommand):
    help = 'Получить chat_id для пользователя'

    def handle(self, *args, **kwargs):
        asyncio.run(self.get_chat_id())

    async def get_chat_id(self):
        bot = Bot(token=settings.TELEGRAM_TOKEN)
        updates = await bot.get_updates()

        if not updates:
            self.stdout.write(self.style.ERROR('Нет обновлений. Проверьте, что бот получает сообщения.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Получено {len(updates)} обновлений'))

        for update in updates:
            if update.message:
                chat_id = update.message.chat_id
                self.stdout.write(self.style.SUCCESS(f'Chat ID: {chat_id}'))
                message = f"Привет! Ваш {chat_id} был успешно получен."
                await bot.send_message(chat_id=chat_id, text=message)
            else:
                self.stdout.write(self.style.WARNING('Нет сообщения в обновлении.'))
