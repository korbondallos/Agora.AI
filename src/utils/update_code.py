# AGORA_BLOCK: start:update_code
import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.code_utils import CodeBlockManager
from src.utils.git_integration import GitIntegration

def update_block(block_id, new_code):
    manager = CodeBlockManager()
    result = manager.replace_block(block_id, new_code)
    print(result)
    
    # Автоматический коммит
    GitIntegration.commit_changes(block_id)
    print("Changes committed to Git")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python src/utils/update_code.py <block_id> <new_code>")
        sys.exit(1)
    
    block_id = sys.argv[1]
    new_code = sys.argv[2]
    
    update_block(block_id, new_code)
# AGORA_BLOCK: end:update_code