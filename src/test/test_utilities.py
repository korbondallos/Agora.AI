# AGORA_BLOCK: start:test_utilities
import sys
import os

# Добавляем корневую директорию проекта в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.code_utils import CodeBlockManager
from utils.git_integration import GitIntegration

def test_code_utils():
    """Тестирование утилит для работы с блоками кода"""
    
    # Инициализация менеджера блоков кода
    manager = CodeBlockManager()
    
    # Тест 1: Получение содержимого блока
    print("=== Тест 1: Получение содержимого блока ===")
    try:
        content = manager.get_block_content("test_block")
        print(f"Текущее содержимое блока:\n{content}")
    except Exception as e:
        print(f"Ошибка при получении содержимого: {e}")
    
    # Тест 2: Замена кода в блоке
    print("\n=== Тест 2: Замена кода в блоке ===")
    new_code = """def hello_world():
    print("Hello, Updated World!")
    return "updated_success"

def new_function():
    print("This is a new function!")
    return "new_success"  # Исправлено: только одна кавычка в конце"""
    
    try:
        result = manager.replace_block("test_block", new_code)
        print(f"Результат замены: {result}")
    except Exception as e:
        print(f"Ошибка при замене кода: {e}")
    
    # Тест 3: Проверка целостности блока
    print("\n=== Тест 3: Проверка целостности блока ===")
    try:
        is_valid, message = manager.validate_block_integrity("test_block")
        print(f"Целостность блока: {is_valid} - {message}")
    except Exception as e:
        print(f"Ошибка при проверке целостности: {e}")
    
    # Тест 4: Проверка целостности всех блоков
    print("\n=== Тест 4: Проверка целостности всех блоков ===")
    try:
        validation_results = manager.validate_all_blocks()
        for block_id, result in validation_results.items():
            status = "✅" if result['valid'] else "❌"
            print(f"{status} {block_id} ({result['layer']}): {result['message']}")
    except Exception as e:
        print(f"Ошибка при проверке всех блоков: {e}")

if __name__ == "__main__":
    test_code_utils()
# AGORA_BLOCK: end:test_utilities
