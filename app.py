import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.enums.chat_action import ChatAction
from handlers import send_welcome, handle_prompt
from openai_client import generate_image

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
# /start и /help
dp.message.register(send_welcome, Command(commands=["start", "help"]))
# основной обработчик
dp.message.register(handle_prompt)

async def main():
    # Проверяем и удаляем любой webhook
    try:
        info = await bot.get_webhook_info()
        logging.info(f"Current webhook URL: {info.url}")
        if info.url:
            await bot.delete_webhook(drop_pending_updates=True)
            logging.info("Deleted existing webhook and dropped pending updates.")
    except Exception as e:
        logging.warning(f"Failed to delete webhook: {e}")

    # Запуск polling с перезапуском при конфликтах
    from aiogram.exceptions import TelegramConflictError
    while True:
        try:
            logging.info("Starting long polling...")
            await dp.start_polling(bot, skip_updates=True)
            break
        except TelegramConflictError as conflict:
            logging.warning(f"Conflict detected: {conflict}. Retrying after webhook deletion...")
            await bot.delete_webhook(drop_pending_updates=True)
        except Exception as e:
            logging.exception(f"Polling failed: {e}")
            await asyncio.sleep(5)
