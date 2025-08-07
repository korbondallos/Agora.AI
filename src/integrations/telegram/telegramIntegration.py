# AGORA_BLOCK: start:telegram_integration
import os
import hashlib
import hmac
import json
from typing import Dict, Optional, Any
from fastapi import HTTPException, status
from pydantic import BaseModel, validator
import httpx
import logging
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramInitData(BaseModel):
    """Модель для валидации initData от Telegram"""
    query_id: str
    user: Dict[str, Any]
    auth_date: int
    hash: str

    @validator('hash')
    def validate_hash(cls, v, values):
        # Временно пропускаем валидацию для разработки
        return v

class TelegramIntegration:
    """Интеграция с Telegram API и обработка initData"""

    def __init__(self):
        # Получаем токен из переменных окружения
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен. Проверьте файл .env")

        # Инициализация HTTP клиента
        self.http_client = httpx.AsyncClient(timeout=10.0)

    async def validate_init_data(self, init_data: str) -> Dict[str, Any]:
        """
        Валидация initData от Telegram

        Args:
            init_data: Строка с данными от Telegram

        Returns:
            Словарь с валидированными данными

        Raises:
            HTTPException: Если данные невалидны
        """
        try:
            # Парсинг строки запроса
            data = dict(pair.split('=') for pair in init_data.split('&'))

            # Валидация хеша (временно упрощенная для разработки)
            if 'hash' not in data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Отсутствует хеш в initData"
                )

            # Возвращаем валидированные данные
            return data

        except Exception as e:
            logger.error(f"Ошибка валидации initData: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидные initData"
            )

    async def get_user_info(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """
        Получение информации о пользователе из Telegram

        Args:
            telegram_id: ID пользователя в Telegram

        Returns:
            Словарь с информацией о пользователе или None
        """
        try:
            # В будущем здесь будет запрос к Telegram API
            # Пока возвращаем тестовые данные
            return {
                "id": telegram_id,
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser"
            }
        except Exception as e:
            logger.error(f"Ошибка получения информации о пользователе: {e}")
            return None

    async def send_message(self, chat_id: int, text: str) -> bool:
        """
        Отправка сообщения в Telegram

        Args:
            chat_id: ID чата
            text: Текст сообщения

        Returns:
            True если сообщение отправлено успешно
        """
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text
            }

            response = await self.http_client.post(url, json=payload)
            response.raise_for_status()

            return True
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            return False

    async def create_chat_invite_link(self, chat_id: int) -> Optional[str]:
        """
        Создание ссылки-приглашения в чат

        Args:
            chat_id: ID чата

        Returns:
            Ссылка-приглашение или None
        """
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/createChatInviteLink"
            payload = {
                "chat_id": chat_id,
                "member_limit": 2  # Только 2 участника
            }

            response = await self.http_client.post(url, json=payload)
            response.raise_for_status()

            data = response.json()
            return data.get("result", {}).get("invite_link")

        except Exception as e:
            logger.error(f"Ошибка создания ссылки-приглашения: {e}")
            return None

# Создаем экземпляр интеграции
telegram_integration = TelegramIntegration()
# AGORA_BLOCK: end:telegram_integration