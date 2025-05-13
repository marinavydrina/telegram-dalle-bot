import logging
from aiogram import types
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from openai_client import generate_image

async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Привет! Напиши простым русским, что ты хочешь нарисовать, "
        "например: «нарисуй улыбающегося робота». Я буду использовать DALL·E-3 и пришлю картинку, как только она будет готова!"
    )

async def handle_prompt(message: types.Message):
    # Игнорируем команды, чтобы не обрабатывать их как промпт
    if message.text and message.text.startswith('/'):
        return

    prompt = message.text.strip()
    if not prompt:
        return

    # Показываем индикатор загрузки
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)

    # Генерируем изображение
    try:
        image_url = generate_image(prompt=prompt)
    except Exception:
        logging.exception("Ошибка при генерации изображения")
        await message.reply("😢 Упс, не получилось сгенерировать картинку. Попробуй чуть позже.")
        return

    # Отправляем картинку
    await message.bot.send_photo(chat_id=message.chat.id, photo=image_url)

# Функция для регистрации хэндлеров
def register_handlers(dp):
    dp.message.register(send_welcome, Command(commands=["start", "help"]))
    dp.message.register(handle_prompt)
