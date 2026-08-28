def filter_by_currency(transactions, currency):
    """Генератор транзакций по валюте."""
    for t in transactions:
        # Безопасное получение вложенного ключа
        if t.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield t


def transaction_descriptions(transactions):
    """Генератор описаний транзакций."""
    for t in transactions:
        yield t.get("description", "")


def card_number_generator(start, stop):
    """Генератор номеров карт в формате XXXX XXXX XXXX XXXX."""
    for num in range(start, stop + 1):
        s = f"{num:016d}"
        yield f"{s[0:4]} {s[4:8]} {s[8:12]} {s[12:16]}"
