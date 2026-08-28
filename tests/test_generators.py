import os
import sys

import pytest

# Настройка пути, чтобы тесты видели src/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
src_path = os.path.join(project_root, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)

from generators import card_number_generator, filter_by_currency, transaction_descriptions  # noqa: E402


@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]


@pytest.mark.parametrize("currency,expected_count", [
    ("USD", 1),
    ("RUB", 1),
    ("EUR", 0),
])
def test_filter_by_currency(transactions, currency, expected_count):
    result = list(filter_by_currency(transactions, currency))
    assert len(result) == expected_count
    if expected_count > 0:
        assert result[0]["operationAmount"]["currency"]["code"] == currency


@pytest.mark.parametrize("input_list,expected_descriptions", [
    ([], []),
    ([{"description": "A"}], ["A"]),
    ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
    ([{"description": "X"}, {}], ["X", ""]),
])
def test_transaction_descriptions(input_list, expected_descriptions):
    result = list(transaction_descriptions(input_list))
    assert result == expected_descriptions


@pytest.mark.parametrize("start,stop,expected", [
    (1, 1, ["0000 0000 0000 0001"]),
    (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    (9999999999999998, 9999999999999999,
     ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
])
def test_card_number_generator(start, stop, expected):
    result = list(card_number_generator(start, stop))
    assert result == expected
