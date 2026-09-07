import pytest
import requests
from unittest.mock import patch
from src.external_api import get_currency_rates, get_stock_prices

@patch("src.external_api.requests.get")
def test_get_currency_rates_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()
    rates = get_currency_rates(["USD", "EUR"])

    # Проверяем, что список не пустой, но все курсы — None
    assert len(rates) == 2
    assert all(r["rate"] is None for r in rates)
    assert rates[0]["currency"] == "USD"
    assert rates[1]["currency"] == "EUR"


@patch("src.external_api.requests.get")
def test_get_stock_prices_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()
    stocks = get_stock_prices(["AAPL", "GOOGL"])

    # Проверяем, что список не пустой, но все цены — None
    assert len(stocks) == 2
    assert all(s["price"] is None for s in stocks)
    assert stocks[0]["stock"] == "AAPL"
    assert stocks[1]["stock"] == "GOOGL"
