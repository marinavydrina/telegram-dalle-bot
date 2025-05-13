import logging
from aiogram import types, Dispatcher
from aiogram.enums import ChatActions
from openai_client import generate_image

# Хэндлер для команд /start и /help
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Привет! Напиши простым русским, что ты хочешь нарисовать, "
        "например: «нарисуй улыбающегося робота». Я буду использовать DALL·E-3 и пришлю картинку, как только она будет готова!"
    )

# Хэндлер для обработки текстовых запросов-промптов
async def handle_prompt(message: types.Message):
    prompt = message.text.strip()
    if not prompt:
        return

    # 1. Показать статус «рисую»
    await message.bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_PHOTO)

    # 2. Сгенерировать картинку
    try:
        image_url = generate_image(
            prompt=prompt,
            model="dall-e-3",
            size="512x512",
            n=1
        )
    except Exception:
        logging.exception("Ошибка при генерации изображения")
        await message.reply("😢 Упс, не получилось сгенерировать картинку. Попробуй чуть позже.")
        return

    # 3. Отправить картинку
    await message.bot.send_photo(chat_id=message.chat.id, photo=image_url)

# Функция для регистрации хэндлеров

def register_handlers(dp: Dispatcher):
    dp.message.register(send_welcome, commands=['start', 'help'])
    dp.message.register(handle_prompt)
