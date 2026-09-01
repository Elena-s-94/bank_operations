import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(
    data_list: List[Dict[str, Any]],
    state: str = "EXECUTED",
) -> List[Dict[str, Any]]:
    """Фильтрует список словарей по состоянию.

    Args:
        data_list (List[Dict[str, Any]]): Список словарей с данными о транзакциях.
        state (str): Состояние для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        List[Dict[str, Any]]: Новый список словарей с указанным состоянием.
    """
    return [item for item in data_list if item.get("state") == state]


def sort_by_date(
    list_data: List[Dict[str, Any]],
    sorted_order: bool = True,
) -> List[Dict[str, Any]]:
    """Сортирует список транзакций по дате.

    Args:
        list_data (List[Dict[str, Any]]): Список словарей с данными о транзакциях.
        sorted_order (bool): Порядок сортировки. По умолчанию True — по убыванию (новые сначала).

    Returns:
        List[Dict[str, Any]]: Отсортированный список словарей.
    """
    return sorted(
        list_data,
        key=lambda x: datetime.fromisoformat(x["date"]),
        reverse=sorted_order,
    )


def process_bank_search(
    data: List[Dict[str, Any]],
    search: str,
) -> List[Dict[str, Any]]:
    """Ищет транзакции по строке в описании с использованием регулярных выражений.

    Поиск регистронезависимый.

    Args:
        data (List[Dict[str, Any]]): Список словарей с транзакциями.
        search (str): Строка для поиска в поле description.

    Returns:
        List[Dict[str, Any]]: Список транзакций, в описании которых найдена искомая строка.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = [t for t in data if pattern.search(t.get("description", ""))]
    return result


def process_bank_operations(
    data: List[Dict[str, Any]],
    categories: List[str],
) -> Dict[str, int]:
    """Подсчитывает количество операций по категориям на основе поля description.

    Использует Counter из collections для подсчёта вхождений.

    Args:
        data (List[Dict[str, Any]]): Список словарей с транзакциями.
        categories (List[str]): Список категорий для подсчёта.

    Returns:
        Dict[str, int]: Словарь, где ключи — названия категорий, значения — количество операций.
    """
    descriptions = [t.get("description", "") for t in data]
    counter = Counter(descriptions)
    return {category: counter.get(category, 0) for category in categories}
