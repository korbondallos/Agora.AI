# AGORA_BLOCK: start:update_code
import sys
import os
import argparse
import pyperclip
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.code_utils import CodeBlockManager
from src.utils.git_integration import GitIntegration

def read_code_from_file(file_path):
    """Чтение кода из файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None

def read_code_from_clipboard():
    """Чтение кода из буфера обмена"""
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"Ошибка чтения из буфера обмена: {e}")
        return None

def read_code_interactive():
    """Интерактивный ввод кода"""
    print("Введите код (завершите пустой строкой):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

def update_block(block_id, new_code, no_commit=False, confirm=False):
    """Обновление блока кода"""
    manager = CodeBlockManager()
    
    if confirm:
        print(f"Будет обновлен блок: {block_id}")
        print(f"Новый код ({len(new_code)} символов):")
        print("-" * 40)
        print(new_code[:200] + "..." if len(new_code) > 200 else new_code)
        print("-" * 40)
        
        response = input("Подтвердить обновление? (y/N): ")
        if response.lower() != 'y':
            print("Обновление отменено")
            return False
    
    try:
        result = manager.replace_block(block_id, new_code)
        print(result)
        
        if not no_commit:
            GitIntegration.commit_changes(block_id)
            print("Changes committed to Git")
        else:
            print("Изменения сохранены без коммита")
        
        return True
    except Exception as e:
        print(f"Ошибка при обновлении блока: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Утилита для обновления блоков кода",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # Из командной строки (для короткого кода)
  python src/utils/update_code.py block_id "print('hello')"

  # Из файла
  python src/utils/update_code.py block_id --file code.txt

  # Из буфера обмена
  python src/utils/update_code.py block_id --clipboard

  # Интерактивный режим
  python src/utils/update_code.py block_id --interactive

  # Без автоматического коммита
  python src/utils/update_code.py block_id --file code.txt --no-commit

  # С подтверждением
  python src/utils/update_code.py block_id --file code.txt --confirm
        """
    )
    
    parser.add_argument('block_id', help='ID блока для обновления')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--code', help='Код для замены (для короткого кода)')
    group.add_argument('--file', '-f', help='Файл с кодом для замены')
    group.add_argument('--clipboard', '-c', action='store_true', help='Взять код из буфера обмена')
    group.add_argument('--interactive', '-i', action='store_true', help='Интерактивный ввод кода')
    
    parser.add_argument('--no-commit', action='store_true', help='Не делать автоматический коммит')
    parser.add_argument('--confirm', action='store_true', help='Запросить подтверждение перед обновлением')
    
    args = parser.parse_args()
    
    # Определяем источник кода
    new_code = None
    
    if args.code:
        new_code = args.code
    elif args.file:
        new_code = read_code_from_file(args.file)
    elif args.clipboard:
        new_code = read_code_from_clipboard()
        if new_code:
            print(f"Код из буфера обмена ({len(new_code)} символов)")
    elif args.interactive:
        new_code = read_code_interactive()
    else:
        # Если не указан источник, пробуем буфер обмена
        new_code = read_code_from_clipboard()
        if not new_code:
            print("Не удалось получить код из буфера обмена, используйте --file, --interactive или --code")
            sys.exit(1)
        else:
            print(f"Код из буфера обмена ({len(new_code)} символов)")
    
    if not new_code:
        print("Не удалось получить код для замены")
        sys.exit(1)
    
    # Обновляем блок
    success = update_block(args.block_id, new_code, args.no_commit, args.confirm)
    
    if success:
        print("Готово!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
# AGORA_BLOCK: end:update_code