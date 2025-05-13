# app.py
import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai

# Из нашего handlers.py
from handlers import register_handlers

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Токены из окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    logging.error("Не заданы TELEGRAM_BOT_TOKEN или OPENAI_API_KEY в окружении")
    exit(1)

# Инициализация клиентов
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPENAI_API_KEY

# Регистрируем все хэндлеры из handlers.py
register_handlers(dp)

if __name__ == '__main__':
    # Запуск long-polling
    executor.start_polling(dp, skip_updates=True)
