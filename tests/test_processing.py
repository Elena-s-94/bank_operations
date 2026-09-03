from datetime import datetime
from src.processing import filter_by_state, sort_by_date

def test_filter_by_state_default():
    data = [
        {"state": "EXECUTED", "id": 1},
        {"state": "PENDING", "id": 2},
        {"state": "EXECUTED", "id": 3},
    ]
    filtered = filter_by_state(data)
    assert len(filtered) == 2
    assert {x["id"] for x in filtered} == {1, 3}

def test_filter_by_state_custom():
    data = [
        {"state": "PENDING", "id": 2},
        {"state": "NEW", "id": 4},
    ]
    filtered = filter_by_state(data, "PENDING")
    assert len(filtered) == 1
    assert filtered[0]["id"] == 2

def test_sort_by_date_desc():
    data = [
        {"date": "2023-01-03T10:00:00"},
        {"date": "2023-01-01T10:00:00"},
        {"date": "2023-01-02T10:00:00"},
    ]
    sorted_data = sort_by_date(data, sorted_order=True)  # по убыванию
    dates = [x["date"] for x in sorted_data]
    assert dates == [
        "2023-01-03T10:00:00",
        "2023-01-02T10:00:00",
        "2023-01-01T10:00:00",
    ]

def test_sort_by_date_asc():
    data = [
        {"date": "2023-01-03T10:00:00"},
        {"date": "2023-01-01T10:00:00"},
        {"date": "2023-01-02T10:00:00"},
    ]
    sorted_data = sort_by_date(data, sorted_order=False)  # по возрастанию
    dates = [x["date"] for x in sorted_data]
    assert dates == [
        "2023-01-01T10:00:00",
        "2023-01-02T10:00:00",
        "2023-01-03T10:00:00",
    ]
