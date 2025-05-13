import os
import logging
import openai

# Инициализируем ключ OpenAI из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("Не задана переменная окружения OPENAI_API_KEY")
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

# Устанавливаем ключ для клиента OpenAI
openai.api_key = OPENAI_API_KEY


def generate_image(
    prompt: str,
    model: str = "dall-e-3",
    size: str = "512x512",
    n: int = 1
) -> str:
    """
    Генерирует изображение по текстовому промпту через OpenAI DALL·E API.

    Args:
        prompt: Текстовый запрос на любом языке.
        model: Название модели (dall-e-3 или dall-e-2).
        size: Размер изображения, например "512x512".
        n: Количество изображений (обычно 1).

    Returns:
        URL первого сгенерированного изображения.

    Raises:
        RuntimeError: При ошибке в API запросе.
    """
    try:
        response = openai.Image.create(
            model=model,
            prompt=prompt,
            size=size,
            n=n
        )
        return response["data"][0]["url"]

    except Exception:
        logging.exception("Ошибка при вызове OpenAI Image API")
        raise RuntimeError("Failed to generate image via OpenAI Image API")
