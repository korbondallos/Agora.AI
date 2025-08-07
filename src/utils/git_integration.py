# AGORA_BLOCK: start:git_integration
# [Описание: Интеграция с Git для автоматического коммита изменений]
# [Зависимости: subprocess]
# [Автор: AI_Assistant / Версия: 1.0]
import subprocess
class GitIntegration:
    @staticmethod
    def commit_changes(block_id, message=None):
        """Автоматический коммит изменений с указанием ID блока"""
        if message is None:
            message = f"AI update: Modified block '{block_id}'"
        
        try:
            # Добавляем измененные файлы
            subprocess.run(["git", "add", "."], check=True)
            
            # Создаем коммит
            subprocess.run(
                ["git", "commit", "-m", message],
                check=True,
                capture_output=True,
                text=True
            )
            
            return f"Changes committed: {message}"
        except subprocess.CalledProcessError as e:
            return f"Git commit failed: {e.stderr}"
# AGORA_BLOCK: end:git_integration
