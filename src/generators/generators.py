from typing import Any, Dict, Generator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]],
    currency: str,
) -> Generator[Dict[str, Any], None, None]:
    """Генератор транзакций, отфильтрованных по коду валюты.

    Проходит по списку транзакций и возвращает только те, у которых
    operationAmount.currency.code совпадает с указанной валютой.

    Args:
        transactions (List[Dict[str, Any]]): список транзакций.
        currency (str): код валюты (например, 'RUB', 'USD').

    Yields:
        Dict[str, Any]: транзакция, соответствующая указанной валюте.
    """
    for t in transactions:
        # Безопасное получение вложенного ключа
        if t.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield t


def transaction_descriptions(
    transactions: List[Dict[str, Any]],
) -> Generator[str, None, None]:
    """Генератор описаний транзакций.

    Извлекает поле description из каждой транзакции. Если описания нет,
    возвращает пустую строку.

    Args:
        transactions (List[Dict[str, Any]]): список транзакций.

    Yields:
        str: описание транзакции или пустая строка.
    """
    for t in transactions:
        yield t.get("description", "")


def card_number_generator(
    start: int,
    stop: int,
) -> Generator[str, None, None]:
    """Генератор номеров карт в формате XXXX XXXX XXXX XXXX.

    Генерирует строки с номерами карт, начиная с `start` и заканчивая `stop`
    (включительно). Каждое число дополняется до 16 цифр нулями слева.

    Args:
        start (int): начальное число.
        stop (int): конечное число (включительно).

    Yields:
        str: номер карты в формате 'XXXX XXXX XXXX XXXX'.
    """
    for num in range(start, stop + 1):
        s = f"{num:016d}"
        yield f"{s[0:4]} {s[4:8]} {s[8:12]} {s[12:16]}"
