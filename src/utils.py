import json
from typing import Any, Dict, List


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с транзакциями.

    Если файл пустой, содержит не список или не найден — возвращает пустой список.

    Args:
        file_path (str): путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: список словарей с данными о транзакциях.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []
