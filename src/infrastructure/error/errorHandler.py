# AGORA_BLOCK: start:error_handler
import logging
import traceback
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Централизованная обработка ошибок"""
    
    @staticmethod
    def handle_error(error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Обработка ошибки и возврат структурированного ответа
        
        Args:
            error: Исключение
            context: Контекст возникновения ошибки
            
        Returns:
            Словарь с информацией об ошибке
        """
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "traceback": traceback.format_exc()
        }
        
        # Логирование ошибки
        logger.error(f"Ошибка в контексте '{context}': {error_info}")
        
        return error_info
    
    @staticmethod
    def log_error(error: Exception, context: str = "") -> None:
        """
        Логирование ошибки без возврата информации
        
        Args:
            error: Исключение
            context: Контекст возникновения ошибки
        """
        logger.error(f"Ошибка в контексте '{context}': {type(error).__name__}: {error}")
# AGORA_BLOCK: end:error_handler