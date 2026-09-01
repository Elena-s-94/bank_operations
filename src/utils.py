import json
import logging
from typing import Any

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_json_file(file_path: str) -> list[dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с транзакциями.

    Если файл пустой, содержит не список или не найден — возвращает пустой список.

    Args:
        file_path: путь к JSON-файлу.

    Returns:
        Список словарей с данными о транзакциях.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            logger.error("Файл %s содержит не список, а %s", file_path, type(data).__name__)
            return []

        logger.info("Файл %s успешно прочитан, найдено %d записей", file_path, len(data))
        return data

    except FileNotFoundError:
        logger.error("Файл %s не найден", file_path)
        return []
    except json.JSONDecodeError:
        logger.error("Файл %s содержит невалидный JSON", file_path)
        return []
