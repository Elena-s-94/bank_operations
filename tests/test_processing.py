from src.processing import process_bank_operations, process_bank_search


def test_process_bank_search_found():
    data = [
        {"description": "Перевод организации", "state": "EXECUTED"},
        {"description": "Открытие вклада", "state": "EXECUTED"},
        {"description": "Перевод с карты на карту", "state": "EXECUTED"},
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 2
    assert result[0]["description"] == "Перевод организации"
    assert result[1]["description"] == "Перевод с карты на карту"


def test_process_bank_search_not_found():
    data = [{"description": "Открытие вклада", "state": "EXECUTED"}]
    result = process_bank_search(data, "покупка")
    assert result == []


def test_process_bank_search_case_insensitive():
    data = [{"description": "ПЕРЕВОД организации", "state": "EXECUTED"}]
    result = process_bank_search(data, "перевод")
    assert len(result) == 1


def test_process_bank_search_empty_data():
    result = process_bank_search([], "перевод")
    assert result == []


def test_process_bank_operations():
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
    ]
    categories = ["Перевод организации", "Открытие вклада", "Неизвестная"]
    result = process_bank_operations(data, categories)
    assert result == {"Перевод организации": 2, "Открытие вклада": 1, "Неизвестная": 0}


def test_process_bank_operations_empty():
    result = process_bank_operations([], ["Перевод", "Вклад"])
    assert result == {"Перевод": 0, "Вклад": 0}


def test_process_bank_operations_no_match():
    data = [{"description": "Открытие вклада"}]
    result = process_bank_operations(data, ["Перевод"])
    assert result == {"Перевод": 0}
