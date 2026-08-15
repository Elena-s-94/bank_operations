from datetime import datetime
from typing import Dict, List


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


def sort_by_date(list_data: list[dict], sorted_order: bool = True)->list[dict]:
    """Параметры:
        data_list (List[Dict]): Список словарей с данными о транзакциях.
        descending (bool): Порядок сортировки. По умолчанию — True (по убыванию).

    Возвращает:
        List[Dict]: Отсортированный список словарей.
    """
    return sorted(list_data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=sorted_order)
