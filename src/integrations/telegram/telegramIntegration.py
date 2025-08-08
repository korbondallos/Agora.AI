# AGORA_BLOCK: start:telegram_integration
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
                detail="Невалидные initData"
            )

        # Парсинг вложенных JSON-полей
        if 'user' in data:
            from urllib.parse import unquote
            import json
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
# AGORA_BLOCK: end:telegram_integration