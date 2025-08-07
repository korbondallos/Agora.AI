# AGORA_BLOCK: start:auth_login
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Dict, Any
import jwt
import datetime
import os

from integrations.telegram.telegramIntegration import telegram_integration
from infrastructure.error.errorHandler import ErrorHandler
from infrastructure.monitoring.monitoringService import monitoring_service

router = APIRouter()
security = HTTPBearer()

class LoginRequest(BaseModel):
    """Модель запроса на вход"""
    init_data: str

class LoginResponse(BaseModel):
    """Модель ответа при успешном входе"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

@router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Эндпоинт для аутентификации через Telegram
    
    Args:
        request: Данные для входа
        
    Returns:
        JWT токен для доступа к API
        
    Raises:
        HTTPException: При ошибках аутентификации
    """
    try:
        # Валидация initData от Telegram
        user_data = await telegram_integration.validate_init_data(request.init_data)
        
        # Получение информации о пользователе
        telegram_id = int(user_data.get('user', {}).get('id'))
        user_info = await telegram_integration.get_user_info(telegram_id)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )
        
        # Создание JWT токена
        payload = {
            "sub": str(telegram_id),
            "user_info": user_info,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        
        token = jwt.encode(
            payload,
            os.getenv("JWT_SECRET", "your-secret-key"),
            algorithm="HS256"
        )
        
        # Логирование успешного входа
        monitoring_service.log_event("auth.success", {"user_id": telegram_id})
        
        return LoginResponse(
            access_token=token,
            expires_in=24 * 60 * 60  # 24 часа в секундах
        )
        
    except Exception as e:
        # Логирование ошибки
        ErrorHandler.handle_error(e, "auth.login")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка аутентификации"
        )

@router.get("/auth/me")
async def get_current_user(token: str = Depends(security)):
    """
    Получение информации о текущем пользователе
    
    Args:
        token: JWT токен
        
    Returns:
        Информация о пользователе
        
    Raises:
        HTTPException: При ошибках валидации токена
    """
    try:
        # Декодирование токена
        payload = jwt.decode(
            token.credentials,
            os.getenv("JWT_SECRET", "your-secret-key"),
            algorithms=["HS256"]
        )
        
        return payload.get("user_info")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен истек"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
# AGORA_BLOCK: end:auth_login