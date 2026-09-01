from unittest.mock import MagicMock, patch

from src.external_api import convert_to_rub


def test_convert_rub_transaction():
    transaction = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {"name": "руб.", "code": "RUB"},
        }
    }
    assert convert_to_rub(transaction) == 1000.50


@patch("src.external_api.requests.get")
def test_convert_usd_transaction(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 90.0}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"name": "USD", "code": "USD"},
        }
    }
    result = convert_to_rub(transaction)
    assert result == 9000.0


@patch("external_api.requests.get")
def test_convert_eur_transaction(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 100.0}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "50",
            "currency": {"name": "EUR", "code": "EUR"},
        }
    }
    result = convert_to_rub(transaction)
    assert result == 5000.0
