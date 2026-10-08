# Вспомогательные функции
import json

from . import decorators


@decorators.handle_db_errors(default={})
def load_metadata(filepath: str) -> dict:
    """
    Загружает данные из JSON-файла
    Если файл не найден, возвращает пустой словарь {}
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

@decorators.handle_db_errors()
def save_metadata(filepath: str, data: dict) -> None:
    """
    Сохраняет переданные данные в JSON-файл
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file)

@decorators.handle_db_errors(default=[])
def load_table_data(table_name: str) -> list:
    """
    Загружает данные по имени таблицы из файла
    """
    with open(f'data/{table_name}.json', 'r', encoding='utf8') as file:
        data = json.load(file)
        return data

@decorators.handle_db_errors()
def save_table_data(table_name: str, data: list) -> None:
    """
    Сохраняет таблицу в файл
    """
    with open(f'data/{table_name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)