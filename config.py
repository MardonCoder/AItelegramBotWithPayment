import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла (если он есть)
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # Токен Telegram-бота
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # API-ключ OpenAI
DB_NAME = "users.db"  # Имя файла базы данных
CLICK_TEST_TOKEN = os.getenv("CLICK_TEST_TOKEN")  # Токен для тестовой оплаты в клик
