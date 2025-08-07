# AGORA_BLOCK: start:interactive_update
import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.code_utils import CodeBlockManager
from src.utils.git_integration import GitIntegration

def interactive_update():
    manager = CodeBlockManager()
    
    print("Доступные блоки:")
    for layer_name, layer in manager.code_map['layers'].items():
        for block_id in layer['modules']:
            print(f"- {block_id} ({layer_name})")
    
    block_id = input("Введите ID блока для обновления: ")
    
    print("Введите новый код (завершите пустой строкой):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    new_code = "\n".join(lines)
    
    result = manager.replace_block(block_id, new_code)
    print(result)
    
    commit = input("Сделать коммит? (y/n): ")
    if commit.lower() == 'y':
        GitIntegration.commit_changes(block_id)
        print("Changes committed to Git")

if __name__ == "__main__":
    interactive_update()
# AGORA_BLOCK: end:interactive_update