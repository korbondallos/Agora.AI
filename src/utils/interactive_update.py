from utils.code_utils import CodeBlockManager
from utils.git_integration import GitIntegration

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
