import asyncio
import os
import sys
import json
from datetime import datetime, timedelta

# Добавляем корневую директорию в sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app
from src.integrations.telegram.telegramIntegration import telegram_integration

def test_auth_api():
    print("Тестирование Auth API...")
    
    # Создаем тестовый клиент
    client = TestClient(app)
    
    # Тест 1: Проверка доступности эндпоинтов
    print("\nТест 1: Проверка доступности эндпоинтов")
    
    # Проверка корневого эндпоинта
    response = client.get("/")
    print(f"✅ Корневой эндпоинт: {response.status_code}")
    
    # Проверка эндпоинта здоровья
    response = client.get("/health")
    print(f"✅ Эндпоинт здоровья: {response.status_code}")
    
    # Тест 2: Попытка входа без данных
    print("\nТест 2: Попытка входа без данных")
    response = client.post("/api/v1/auth/login", json={})
    print(f"✅ Ошибка валидации: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    
    # Тест 3: Вход с неверными данными
    print("\nТест 3: Вход с неверными данными")
    invalid_data = {
        "init_data": "invalid_data"
    }
    response = client.post("/api/v1/auth/login", json=invalid_data)
    print(f"✅ Ошибка аутентификации: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    
    # Тест 4: Вход с тестовыми данными
    print("\nТест 4: Вход с тестовыми данными")
    test_init_data = "query_id=AAHdF6IQAAAAAN0XohDhrKY&user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22User%22%2C%22username%22%3A%22testuser%22%2C%22language_code%22%3A%22en%22%7D&auth_date=1663224242&hash=c8a3b9e3d8e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1"
    
    login_data = {
        "init_data": test_init_data
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    print(f"✅ Статус входа: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"   Токен получен: {token_data.get('access_token', '')[:20]}...")
        print(f"   Тип токена: {token_data.get('token_type')}")
        print(f"   Время жизни: {token_data.get('expires_in')} секунд")
        
        # Тест 5: Проверка токена
        print("\nТест 5: Проверка токена")
        token = token_data.get('access_token')
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/auth/me", headers=headers)
        print(f"✅ Получение данных пользователя: {response.status_code}")
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"   User ID: {user_info.get('id')}")
            print(f"   First Name: {user_info.get('first_name')}")
            print(f"   Username: {user_info.get('username')}")
        else:
            print(f"   Ошибка: {response.json()}")
    else:
        print(f"   Ошибка входа: {response.json()}")

if __name__ == "__main__":
    test_auth_api()