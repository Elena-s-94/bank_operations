import pytest


@pytest.fixture
def sample_card_numbers():
    """Возвращает список номеров карт для тестов."""
    return [
        "7000792289606361",
        "1234567890123456",
        "1111222233334444",
    ]


@pytest.fixture
def sample_account_numbers():
    """Возвращает список номеров счетов для тестов."""
    return [
        "73654108430135874319",
        "12345678901234567890",
    ]


@pytest.fixture
def sample_dict_list():
    """Список словарей для тестов processing."""
    return [
        {"id": 4231, "state": "EXECUTED", "date": "2024-06-05T14:30:20.72"},
        {"id": 9612, "state": "CANCELED", "date": "2024-01-15T10:20:05.12"},
        {"id": 1543, "state": "EXECUTED", "date": "2023-12-01T08:15:00.00"},
        {"id": 7543, "state": "CANCELED", "date": "2024-03-10T12:00:00.00"},
    ]


@pytest.fixture
def same_date_list():
    """Список словарей с одинаковыми датами."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T00:00:00.00"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01T00:00:00.00"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-01T00:00:00.00"},
    ]
