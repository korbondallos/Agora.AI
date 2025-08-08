# AGORA_FILE: start:src/infrastructure/error/errorHandler.py
# AGORA_BLOCK: start:error_handler
import logging
import traceback
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# AGORA_BLOCK: start:error_handler_class
class ErrorHandler:
    """Централизованная обработка ошибок"""
    
    # AGORA_BLOCK: start:handle_error
    @staticmethod
    def handle_error(error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Обработка ошибки и возврат структурированного ответа
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
    # AGORA_BLOCK: end:handle_error
    
    # AGORA_BLOCK: start:log_error
    @staticmethod
    def log_error(error: Exception, context: str = "") -> None:
        """
        Логирование ошибки без возврата информации
        """
        logger.error(f"Ошибка в контексте '{context}': {type(error).__name__}: {error}")
    # AGORA_BLOCK: end:log_error
# AGORA_BLOCK: end:error_handler_class
# AGORA_BLOCK: end:error_handler
# AGORA_FILE: end:src/infrastructure/error/errorHandler.py
