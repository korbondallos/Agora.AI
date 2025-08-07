# AGORA_BLOCK: start:code_utils
# [Описание: Утилиты для работы с тегированными блоками кода]
# [Зависимости: json, os, re, datetime]
# [Автор: AI_Assistant / Версия: 1.0]
import json
import os
import re
from datetime import datetime
class CodeBlockManager:
    def __init__(self, code_map_path="docs/architecture/code_map.json"):
        self.code_map_path = code_map_path
        self.code_map = self._load_code_map()
    
    def _load_code_map(self):
        """Загрузка кодовой карты из JSON файла"""
        if not os.path.exists(self.code_map_path):
            raise FileNotFoundError(f"Code map file not found: {self.code_map_path}")
        
        with open(self.code_map_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_code_map(self):
        """Сохранение кодовой карты в JSON файл"""
        with open(self.code_map_path, 'w', encoding='utf-8') as f:
            json.dump(self.code_map, f, indent=2, ensure_ascii=False)
    
    def get_block_info(self, block_id):
        """Получение информации о блоке по ID"""
        for layer in self.code_map['layers'].values():
            if block_id in layer['modules']:
                return layer['modules'][block_id]
        raise ValueError(f"Block with ID '{block_id}' not found in code map")
    
    def find_block_in_file(self, file_path, start_tag, end_tag):
        """Поиск границ блока в файле"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        
        start_idx = None
        end_idx = None
        
        for i, line in enumerate(lines):
            if start_tag in line:
                start_idx = i
            if end_tag in line and start_idx is not None:
                end_idx = i
                break
        
        if start_idx is None or end_idx is None:
            raise ValueError(f"Block tags not found in file: {file_path}")
        
        return start_idx, end_idx, lines
    
    def replace_block(self, block_id, new_code, update_metadata=True):
        """Замена кода в указанном блоке"""
        block_info = self.get_block_info(block_id)
        
        start_idx, end_idx, lines = self.find_block_in_file(
            block_info['file'], 
            block_info['start_tag'], 
            block_info['end_tag']
        )
        
        # Формируем новый контент блока с сохранением тегов
        new_lines = (
            lines[:start_idx + 1] +  # Сохраняем start_tag
            [new_code + '\n'] +      # Новый код
            lines[end_idx:]          # Сохраняем end_tag и остальной файл
        )
        
        # Записываем изменения в файл
        with open(block_info['file'], 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        # Обновляем метаданные
        if update_metadata:
            block_info['last_modified'] = datetime.now().isoformat()
            block_info['version'] = self._increment_version(block_info['version'])
            self._save_code_map()
        
        return f"Block '{block_id}' successfully updated in {block_info['file']}"
    
    def get_block_content(self, block_id):
        """Получение текущего содержимого блока"""
        block_info = self.get_block_info(block_id)
        
        start_idx, end_idx, lines = self.find_block_in_file(
            block_info['file'], 
            block_info['start_tag'], 
            block_info['end_tag']
        )
        
        # Извлекаем контент между тегами (без самих тегов)
        block_lines = lines[start_idx + 1 : end_idx]
        return ''.join(block_lines).strip()
    
    def validate_block_integrity(self, block_id):
        """Проверка целостности блока (наличие обоих тегов)"""
        block_info = self.get_block_info(block_id)
        
        try:
            self.find_block_in_file(
                block_info['file'], 
                block_info['start_tag'], 
                block_info['end_tag']
            )
            return True, "Block integrity validated"
        except ValueError as e:
            return False, str(e)
    
    def validate_all_blocks(self):
        """Проверка целостности всех блоков"""
        results = {}
        for layer_name, layer in self.code_map['layers'].items():
            for block_id in layer['modules']:
                is_valid, message = self.validate_block_integrity(block_id)
                results[block_id] = {
                    'valid': is_valid,
                    'message': message,
                    'layer': layer_name
                }
        return results
    
    def _increment_version(self, version):
        """Инкремент версии (семантическое версионирование)"""
        try:
            major, minor, patch = map(int, version.split('.'))
            return f"{major}.{minor}.{patch + 1}"
        except:
            return "1.0.0"
    
    def create_new_block(self, block_id, file_path, start_tag, end_tag, description, layer, dependencies=None):
        """Создание нового блока в кодовой карте"""
        if dependencies is None:
            dependencies = []
        
        # Определяем слой для добавления
        if layer not in self.code_map['layers']:
            raise ValueError(f"Layer '{layer}' not found in code map")
        
        # Проверяем уникальность ID
        for l in self.code_map['layers'].values():
            if block_id in l['modules']:
                raise ValueError(f"Block ID '{block_id}' already exists")
        
        # Создаем запись о новом блоке
        new_block = {
            "id": block_id,
            "file": file_path,
            "start_tag": start_tag,
            "end_tag": end_tag,
            "description": description,
            "dependencies": dependencies,
            "author": "AI_Assistant",
            "version": "1.0.0",
            "last_modified": datetime.now().isoformat()
        }
        
        self.code_map['layers'][layer]['modules'][block_id] = new_block
        self._save_code_map()
        
        return f"New block '{block_id}' created in layer '{layer}'"
# Пример использования
if __name__ == "__main__":
    # Инициализация менеджера
    manager = CodeBlockManager()
    
    # Пример замены кода в блоке
    try:
        result = manager.replace_block(
            block_id="matchmaking_engine",
            new_code="def match_companies(company_a, company_b):\n    # Новая реализация\n    return True"
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    
    # Пример проверки целостности всех блоков
    validation_results = manager.validate_all_blocks()
    for block_id, result in validation_results.items():
        status = "✅" if result['valid'] else "❌"
        print(f"{status} {block_id} ({result['layer']}): {result['message']}")
# AGORA_BLOCK: end:code_utils
