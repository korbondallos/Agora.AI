import asyncio
import os
import json
from dotenv import load_dotenv
from src.integrations.telegram.telegramIntegration import telegram_integration

async def test_telegram_real():
    # Проверяем наличие токена
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден в .env файле")
        return
    
    print(f"✅ Токен бота найден: {bot_token[:10]}...")
    
    # Реальные initData от Telegram (пример)
    real_init_data = "query_id=AAHdF6IQAAAAAN0XohDhrKY&user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22User%22%2C%22username%22%3A%22testuser%22%2C%22language_code%22%3A%22en%22%7D&auth_date=1663224242&hash=c8a3b9e3d8e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1"

    try:
        # Тест 1: Валидация реальных initData
        print("\nТест 1: Валидация initData")
        user_data = await telegram_integration.validate_init_data(real_init_data)
        print(f"✅ Валидация успешна")
        
        # Теперь user_data['user'] уже распарсен в объект
        user_info = user_data.get('user', {})
        print(f"   User ID: {user_info.get('id')}")
        print(f"   First Name: {user_info.get('first_name')}")
        print(f"   Username: {user_info.get('username')}")

        # Тест 2: Получение информации о пользователе
        print("\nТест 2: Получение информации о пользователе")
        user_id = user_info.get('id')
        user_info = await telegram_integration.get_user_info(user_id)
        print(f"✅ Информация о пользователе получена")
        print(f"   {user_info}")

        # Тест 3: Проверка подключения к Telegram API
        print("\nТест 3: Проверка подключения к Telegram API")
        try:
            # Получим информацию о боте
            bot_info_url = f"https://api.telegram.org/bot{bot_token}/getMe"
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(bot_info_url)
                if response.status_code == 200:
                    bot_info = response.json()
                    print(f"✅ Подключение к Telegram API успешно")
                    print(f"   Бот: @{bot_info['result']['username']}")
                    print(f"   Имя: {bot_info['result']['first_name']}")
                else:
                    print(f"❌ Ошибка подключения к Telegram API: {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка при проверке подключения: {e}")

        # Тест 4: Отправка сообщения (если бот запущен)
        print("\nТест 4: Отправка тестового сообщения")
        try:
            # Замените на ваш реальный chat_id или используйте user_id из теста
            chat_id = user_id  # Это не сработает для реального бота, нужен реальный chat_id
            result = await telegram_integration.send_message(chat_id, "Тестовое сообщение от Agora.AI")
            print(f"✅ Сообщение отправлено успешно")
        except Exception as e:
            print(f"⚠️  Не удалось отправить сообщение: {e}")
            print("   Это нормально, если у вас нет реального chat_id")

        # Тест 5: Создание ссылки-приглашения
        print("\nТест 5: Создание ссылки-приглашения")
        try:
            # Замените на реальный chat_id группы
            chat_id = -1001234567890  # Пример ID группы (отрицательное число)
            invite_link = await telegram_integration.create_chat_invite_link(chat_id)
            print(f"✅ Ссылка-приглашение создана: {invite_link}")
        except Exception as e:
            print(f"⚠️  Не удалось создать ссылку-приглашение: {e}")
            print("   Это нормально, если у вас нет реального chat_id группы")

    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    load_dotenv()
    print("Начинаем тестирование Telegram интеграции...")
    asyncio.run(test_telegram_real())