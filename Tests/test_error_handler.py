import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.infrastructure.error.errorHandler import ErrorHandler

def test_error_handler():
    print("Тестирование ErrorHandler...")
    
    # Тест 1: Базовая обработка ошибки
    print("\nТест 1: Базовая обработка ошибки")
    try:
        raise ValueError("Тестовая ошибка значения")
    except Exception as e:
        error_info = ErrorHandler.handle_error(e, "test_context")
        print(f"✅ Ошибка обработана: {error_info['error_type']}")
        print(f"   Контекст: {error_info['context']}")
        print(f"   Сообщение: {error_info['error_message']}")
    
    # Тест 2: Логирование ошибки
    print("\nТест 2: Логирование ошибки")
    try:
        raise RuntimeError("Тестовая ошибка времени выполнения")
    except Exception as e:
        ErrorHandler.log_error(e, "runtime_test")
        print("✅ Ошибка залогирована")
    
    # Тест 3: Обработка разных типов исключений
    print("\nТест 3: Разные типы исключений")
    exceptions_to_test = [
        ValueError("Ошибка значения"),
        RuntimeError("Ошибка времени выполнения"),
        KeyError("Ошибка ключа"),
        FileNotFoundError("Файл не найден")
    ]
    
    for i, exc in enumerate(exceptions_to_test, 1):
        try:
            raise exc
        except Exception as e:
            error_info = ErrorHandler.handle_error(e, f"test_{i}")
            print(f"✅ {type(e).__name__}: {error_info['error_type']}")

if __name__ == "__main__":
    test_error_handler()