import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(
    data_list: List[Dict],
    state: str = "EXECUTED",
) -> List[Dict]:
    """Фильтрует список словарей по состоянию.

    Параметры:
        data_list (List[Dict]): Список словарей с данными о транзакциях.
        state (str): Состояние для фильтрации (по умолчанию 'EXECUTED').

    Возвращает:
        List[Dict]: Новый список словарей с указанным состоянием.
    """
    return [item for item in data_list if item.get("state") == state]


def sort_by_date(list_data: list[dict], sorted_order: bool = True) -> list[dict]:
    """Параметры:
        data_list (List[Dict]): Список словарей с данными о транзакциях.
        descending (bool): Порядок сортировки. По умолчанию — True (по убыванию).

    Возвращает:
        List[Dict]: Отсортированный список словарей.
    """
    return sorted(list_data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=sorted_order)


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Ищет транзакции по строке в описании с использованием регулярных выражений.

    Args:
        data: список словарей с транзакциями.
        search: строка для поиска в описании.

    Returns:
        Список словарей с транзакциями, в описании которых есть искомая строка.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = [t for t in data if pattern.search(t.get("description", ""))]
    return result


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество операций по категориям на основе поля description.

    Использует Counter из collections для подсчёта.

    Args:
        data: список словарей с транзакциями.
        categories: список категорий для подсчёта.

    Returns:
        Словарь, где ключи — названия категорий, значения — количество операций.
    """
    descriptions = [t.get("description", "") for t in data]
    counter = Counter(descriptions)
    return {category: counter.get(category, 0) for category in categories}
