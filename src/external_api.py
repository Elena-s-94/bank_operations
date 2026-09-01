import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли.

    Если транзакция в USD или EUR — обращается к внешнему API для получения курса.
    Если транзакция уже в рублях — возвращает сумму без изменений.

    Args:
        transaction (Dict[str, Any]): словарь с данными о транзакции.

    Returns:
        float: сумма транзакции в рублях.
    """
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    headers = {"apikey": API_KEY}
    params = {"base": currency, "symbols": "RUB"}
    response = requests.get(URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    rate = response.json()["rates"]["RUB"]

    return round(amount * rate, 2)
