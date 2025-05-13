import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from handlers import register_handlers
import openai_client

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Чтение токенов из окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    logging.error("Не заданы TELEGRAM_BOT_TOKEN или OPENAI_API_KEY")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Регистрируем хэндлеры
register_handlers(dp)

async def main():
    # Удаляем возможный webhook, чтобы начать long polling без конфликтов
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Webhook deleted, starting polling...")

    # Запуск polling
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
