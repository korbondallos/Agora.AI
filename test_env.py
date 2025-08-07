import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

print("TELEGRAM_BOT_TOKEN:", os.getenv("TELEGRAM_BOT_TOKEN"))
print("JWT_SECRET:", os.getenv("JWT_SECRET"))