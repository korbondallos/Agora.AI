# AGORA_BLOCK: start:update_code
import sys
import os
import argparse
import pyperclip
import re
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.code_utils import CodeBlockManager
from src.utils.git_integration import GitIntegration

def clean_code(code):
    """Очистка кода от лишних пустых строк и нормализация переносов"""
    if not code:
        return code
    
    # Разделяем на строки
    lines = code.splitlines()
    
    # Удаляем пустые строки в начале и конце
    while lines and lines[0].strip() == '':
        lines.pop(0)
    while lines and lines[-1].strip() == '':
        lines.pop()
    
    # Нормализуем пустые строки (оставляем только по одной пустой строке между блоками)
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        is_empty = line.strip() == ''
        
        # Добавляем пустую строку только если предыдущая не была пустой
        if is_empty and not prev_empty:
            cleaned_lines.append('')
        elif not is_empty:
            cleaned_lines.append(line)
        
        prev_empty = is_empty
    
    # Удаляем последнюю пустую строку, если она есть
    if cleaned_lines and cleaned_lines[-1] == '':
        cleaned_lines.pop()
    
    # Объединяем с правильными переносами строк
    return '\n'.join(cleaned_lines)

def find_block_by_tag(tag_name):
    """Найти блок по тегу"""
    manager = CodeBlockManager()
    
    # Поддерживаем оба формата: с префиксом и без
    possible_tags = [
        f"# AGORA_BLOCK: start:{tag_name}",
        tag_name if tag_name.startswith("# AGORA_BLOCK: start:") else None
    ]
    
    for full_tag in possible_tags:
        if full_tag is None:
            continue
            
        for layer_name, layer in manager.code_map['layers'].items():
            for block_id, block_info in layer['modules'].items():
                if block_info['start_tag'] == full_tag:
                    return block_id
    
    return None

def read_code_from_file(file_path):
    """Чтение кода из файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            return clean_code(code)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None

def read_code_from_clipboard():
    """Чтение кода из буфера обмена"""
    try:
        code = pyperclip.paste()
        return clean_code(code)
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
    return clean_code('\n'.join(lines))

def update_block(block_id, new_code, no_commit=False, confirm=False, dry_run=False):
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
    
    if dry_run:
        print(f"[DRY RUN] Блок {block_id} будет обновлен")
        print(f"Новый код ({len(new_code)} символов):")
        print("-" * 40)
        print(new_code)
        print("-" * 40)
        return True
    
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
        description="Утилита для обновления блоков кода по тегам",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # По тегу (рекомендуется)
  python src/utils/update_code.py --tag monitoring_service --clipboard
  python src/utils/update_code.py -t telegram_integration --file code.txt

  # По ID (старый способ)
  python src/utils/update_code.py block_id --clipboard

  # Другие опции
  python src/utils/update_code.py --tag monitoring_service --interactive --confirm
  python src/utils/update_code.py --tag monitoring_service --file code.txt --dry-run

Поддерживаемые форматы тегов:
  - Короткий: monitoring_service
  - Полный: "# AGORA_BLOCK: start:monitoring_service"
        """
    )
    
    # Группа для идентификации блока (ID или тег)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('block_id', nargs='?', help='ID блока для обновления (старый способ)')
    group.add_argument('--tag', '-t', help='Тег блока (рекомендуется)')
    
    # Группа для источника кода
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument('--code', help='Код для замены (для короткого кода)')
    source_group.add_argument('--file', '-f', help='Файл с кодом для замены')
    source_group.add_argument('--clipboard', '-c', action='store_true', help='Взять код из буфера обмена')
    source_group.add_argument('--interactive', '-i', action='store_true', help='Интерактивный ввод кода')
    
    # Опции управления
    parser.add_argument('--no-commit', action='store_true', help='Не делать автоматический коммит')
    parser.add_argument('--confirm', action='store_true', help='Запросить подтверждение перед обновлением')
    parser.add_argument('--dry-run', action='store_true', help='Тестовый запуск без реальных изменений')
    
    args = parser.parse_args()
    
    # Определяем блок для обновления
    block_id = None
    
    if args.tag:
        # Ищем блок по тегу
        block_id = find_block_by_tag(args.tag)
        if not block_id:
            print(f"Ошибка: Блок с тегом '{args.tag}' не найден")
            print("Проверьте правильность тега или используйте список доступных тегов")
            sys.exit(1)
        print(f"Найден блок: {block_id} (по тегу: {args.tag})")
    else:
        block_id = args.block_id
    
    # Определяем источник кода
    new_code = None
    
    if args.code:
        new_code = clean_code(args.code)
    elif args.file:
        new_code = read_code_from_file(args.file)
    elif args.clipboard:
        new_code = read_code_from_clipboard()
        if new_code:
            print(f"Код из буфера обмена ({len(new_code)} символов) - очищен")
    elif args.interactive:
        new_code = read_code_interactive()
    else:
        # По умолчанию пробуем буфер обмена
        new_code = read_code_from_clipboard()
        if not new_code:
            print("Не удалось получить код из буфера обмена, используйте --file, --interactive или --code")
            sys.exit(1)
        else:
            print(f"Код из буфера обмена ({len(new_code)} символов) - очищен")
    
    if not new_code:
        print("Не удалось получить код для замены")
        sys.exit(1)
    
    # Обновляем блок
    success = update_block(block_id, new_code, args.no_commit, args.confirm, args.dry_run)
    
    if success:
        print("Готово!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
# AGORA_BLOCK: end:update_code