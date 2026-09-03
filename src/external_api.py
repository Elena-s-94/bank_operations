"""Модуль для получения курсов валют и цен на акции через внешние API."""

import logging
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает курсы валют через бесплатное API.

    Args:
        currencies (List[str]): список кодов валют, например ['USD', 'EUR'].

    Returns:
        List[Dict[str, Any]]: список словарей с ключами 'currency' и 'rate'.
    """
    result = []
    try:
        url = "https://open.er-api.com/v6/latest/RUB"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})

        for currency in currencies:
            rate = rates.get(currency)
            if rate and rate > 0:
                # API возвращает курс RUB -> валюту, нам нужен обратный
                result.append({"currency": currency, "rate": round(1 / rate, 2)})
            else:
                logger.warning("Курс для %s не найден", currency)
                result.append({"currency": currency, "rate": None})
    except requests.RequestException as e:
        logger.error("Ошибка при получении курсов валют: %s", e)
        for currency in currencies:
            result.append({"currency": currency, "rate": None})
    return result


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает цены на акции через Yahoo Finance API.

    Args:
        stocks (List[str]): список тикеров, например ['AAPL', 'AMZN'].

    Returns:
        List[Dict[str, Any]]: список словарей с ключами 'stock' и 'price'.
    """
    result = []
    for stock in stocks:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = data.get("chart", {}).get("result", [{}])[0].get("meta", {}).get("regularMarketPrice")
            if price and price > 0:
                result.append({"stock": stock, "price": round(float(price), 2)})
            else:
                logger.warning("Цена для %s не найдена", stock)
                result.append({"stock": stock, "price": None})
        except (requests.RequestException, IndexError, KeyError, ValueError) as e:
            logger.error("Ошибка при получении цены акции %s: %s", stock, e)
            result.append({"stock": stock, "price": None})
    return result
