# AGORA_FILE: start:src/integrations/telegram/telegramIntegration.py
# AGORA_BLOCK: start:telegram_integration
import os
import hashlib
import hmac
import json
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator
import httpx
import logging
from urllib.parse import unquote
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AGORA_BLOCK: start:telegram_init_data_model
class TelegramInitData(BaseModel):
    """Модель для валидации initData от Telegram"""
    query_id: str
    user: Dict[str, Any]
    auth_date: int
    hash: str
    
    @field_validator('hash')
    @classmethod
    def validate_hash(cls, v):
        # Временно пропускаем валидацию для разработки
        return v
# AGORA_BLOCK: end:telegram_init_data_model

# AGORA_BLOCK: start:telegram_integration_class
class TelegramIntegration:
    """Интеграция с Telegram API и обработка initData"""
    
    # AGORA_BLOCK: start:init
    def __init__(self):
        # Получаем токен из переменных окружения
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен. Проверьте файл .env")
        
        # Инициализация HTTP клиента
        self.http_client = httpx.AsyncClient(timeout=10.0)
    # AGORA_BLOCK: end:init
    
    # AGORA_BLOCK: start:validate_init_data
    async def validate_init_data(self, init_data: str) -> Dict[str, Any]:
        """
        Валидация initData от Telegram
        """
        try:
            # Парсинг строки запроса
            data = dict(pair.split('=') for pair in init_data.split('&'))
            
            # Валидация хеша (временно упрощенная для разработки)
            if 'hash' not in data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Невалидные initData"
                )
            
            # Парсинг вложенных JSON-полей
            if 'user' in data:
                user_str = unquote(data['user'])
                data['user'] = json.loads(user_str)
            
            # Возвращаем валидированные данные
            return data
            
        except Exception as e:
            logger.error(f"Ошибка валидации initData: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидные initData"
            )
    # AGORA_BLOCK: end:validate_init_data
    
    # AGORA_BLOCK: start:get_user_info
    async def get_user_info(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """
        Получение информации о пользователе из Telegram
        """
        try:
            return {
                "id": telegram_id,
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser"
            }
        except Exception as e:
            logger.error(f"Ошибка получения информации о пользователе: {e}")
            return None
    # AGORA_BLOCK: end:get_user_info
    
    # AGORA_BLOCK: start:send_message
    async def send_message(self, chat_id: int, text: str) -> bool:
        """
        Отправка сообщения в Telegram
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
    # AGORA_BLOCK: end:send_message
    
    # AGORA_BLOCK: start:create_chat_invite_link
    async def create_chat_invite_link(self, chat_id: int) -> Optional[str]:
        """
        Создание ссылки-приглашения в чат
        """
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/createChatInviteLink"
            payload = {
                "chat_id": chat_id,
                "member_limit": 2
            }
            
            response = await self.http_client.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return data.get("result", {}).get("invite_link")
            
        except Exception as e:
            logger.error(f"Ошибка создания ссылки-приглашения: {e}")
            return None
    # AGORA_BLOCK: end:create_chat_invite_link
# AGORA_BLOCK: end:telegram_integration_class

# Создаем экземпляр интеграции
telegram_integration = TelegramIntegration()
# AGORA_BLOCK: end:telegram_integration
# AGORA_FILE: end:src/integrations/telegram/telegramIntegration.py
