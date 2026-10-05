# Вспомогательные функции
import json


def load_metadata(filepath: str) -> dict:
    """
    Загружает данные из JSON-файла
    Если файл не найден, возвращает пустой словарь {}
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

def save_metadata(filepath: str, data: dict) -> None:
    """
    Сохраняет переданные данные в JSON-файл
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file)