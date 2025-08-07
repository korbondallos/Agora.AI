# AGORA_BLOCK: start:project_structure_exporter
import os
import datetime
from typing import List, Set

class ProjectStructureExporter:
    def __init__(self, root_path: str = ".", output_file: str = "project_structure.txt"):
        self.root_path = os.path.abspath(root_path)
        self.output_file = output_file
        self.text_extensions = {'.py', '.txt', '.json', '.md', '.yml', '.yaml', '.env', '.ini', '.cfg', '.toml', '.xml', '.html', '.css', '.js', '.sql', '.sh', '.bat', '.ps1', '.gitignore', '.dockerignore'}
        self.skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.vscode', '.idea', 'venv', 'env', 'dist', 'build'}
        
    def should_skip_directory(self, dir_name: str) -> bool:
        """Проверить, нужно ли пропустить директорию"""
        return dir_name in self.skip_dirs or dir_name.startswith('.')
    
    def should_read_file(self, file_path: str) -> bool:
        """Проверить, нужно ли читать содержимое файла"""
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.text_extensions
    
    def get_directory_structure(self, path: str, prefix: str = "") -> List[str]:
        """Рекурсивно получить структуру директорий"""
        structure = []
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return structure
        
        dirs = []
        files = []
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                if not self.should_skip_directory(item):
                    dirs.append(item)
            else:
                files.append(item)
        
        # Сначала директории
        for i, dir_name in enumerate(dirs):
            is_last_dir = i == len(dirs) - 1 and len(files) == 0
            current_prefix = "└── " if is_last_dir else "├── "
            structure.append(prefix + current_prefix + dir_name + "/")
            
            next_prefix = prefix + ("    " if is_last_dir else "│   ")
            structure.extend(self.get_directory_structure(os.path.join(path, dir_name), next_prefix))
        
        # Затем файлы
        for i, file_name in enumerate(files):
            is_last_file = i == len(files) - 1
            current_prefix = "└── " if is_last_file else "├── "
            structure.append(prefix + current_prefix + file_name)
        
        return structure
    
    def read_file_content(self, file_path: str) -> str:
        """Прочитать содержимое файла с обработкой ошибок"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                return f"[Ошибка чтения файла: {str(e)}]"
        except Exception as e:
            return f"[Ошибка чтения файла: {str(e)}]"
    
    def export_project(self):
        """Основной метод экспорта проекта"""
        print(f"Начинаю экспорт структуры проекта из: {self.root_path}")
        print(f"Результат будет сохранен в: {self.output_file}")
        
        # Получаем структуру директорий
        structure_lines = self.get_directory_structure(self.root_path)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # Заголовок
            f.write("=" * 80 + "\n")
            f.write("СТРУКТУРА ПРОЕКТА\n")
            f.write("=" * 80 + "\n")
            f.write(f"Дата создания: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Корневая директория: {self.root_path}\n")
            f.write("=" * 80 + "\n\n")
            
            # Иерархия папок и файлов
            f.write("ИЕРАРХИЯ ПАПОК И ФАЙЛОВ:\n")
            f.write("-" * 40 + "\n")
            for line in structure_lines:
                f.write(line + "\n")
            f.write("\n" + "=" * 80 + "\n\n")
            
            # Содержимое файлов
            f.write("СОДЕРЖИМОЕ ФАЙЛОВ:\n")
            f.write("-" * 40 + "\n")
            
            # Собираем все файлы для обработки
            all_files = []
            for root, dirs, files in os.walk(self.root_path):
                # Пропускаем нежелательные директории
                dirs[:] = [d for d in dirs if not self.should_skip_directory(d)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.root_path)
                    all_files.append((relative_path, file_path))
            
            # Сортируем файлы по пути
            all_files.sort(key=lambda x: x[0])
            
            # Записываем содержимое каждого файла
            for relative_path, file_path in all_files:
                if self.should_read_file(file_path):
                    f.write(f"\n{'='*80}\n")
                    f.write(f"ФАЙЛ: {relative_path}\n")
                    f.write(f"{'='*80}\n")
                    content = self.read_file_content(file_path)
                    f.write(content)
                    if not content.endswith('\n'):
                        f.write('\n')
                else:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"ФАЙЛ: {relative_path}\n")
                    f.write(f"{'='*80}\n")
                    f.write(f"[БИНАРНЫЙ ФАЙЛ - СОДЕРЖИМОЕ НЕ ПРОЧИТАНО]\n")
        
        print(f"Экспорт завершен! Результат сохранен в файл: {self.output_file}")
        print(f"Размер файла: {os.path.getsize(self.output_file)} байт")

def main():
    """Основная функция для запуска утилиты"""
    print("Утилита экспорта структуры проекта")
    print("=" * 50)
    
    # Создаем экспортер
    exporter = ProjectStructureExporter()
    
    # Запускаем экспорт
    exporter.export_project()

if __name__ == "__main__":
    main()
# AGORA_BLOCK: end:project_structure_exporter