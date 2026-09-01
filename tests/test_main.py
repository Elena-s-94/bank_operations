from unittest.mock import mock_open, patch

from main import main


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"id": 1, "state": "EXECUTED", "date": "2019-12-08T22:35:35", '
    '"description": "Открытие вклада", "operationAmount": {"amount": "40542", '
    '"currency": {"name": "руб.", "code": "RUB"}}, "to": "Счет 6543210987654321"}]',
)
def test_main_json_success(mock_open_func, capsys, monkeypatch):
    inputs = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Привет" in captured.out
    assert "JSON" in captured.out
    assert "EXECUTED" in captured.out
    assert "Открытие вклада" in captured.out
    assert "40542" in captured.out


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"id": 1, "state": "EXECUTED", "date": "2019-12-08T22:35:35", '
    '"description": "Открытие вклада", "operationAmount": {"amount": "40542", '
    '"currency": {"name": "руб.", "code": "RUB"}}, "to": "Счет 6543210987654321"}]',
)
def test_main_invalid_status_then_valid(mock_open_func, capsys, monkeypatch):
    inputs = iter(["1", "test", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "недоступен" in captured.out
    assert "EXECUTED" in captured.out


@patch("builtins.open", new_callable=mock_open, read_data="[]")
def test_main_empty_result(mock_open_func, capsys, monkeypatch):
    inputs = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"id": 1, "state": "EXECUTED", "date": "2019-12-08T22:35:35", '
    '"description": "Открытие вклада", "operationAmount": {"amount": "40542", '
    '"currency": {"name": "руб.", "code": "RUB"}}, "to": "Счет 6543210987654321"},'
    '{"id": 2, "state": "EXECUTED", "date": "2020-01-15T10:00:00", '
    '"description": "Перевод", "operationAmount": {"amount": "100", '
    '"currency": {"name": "USD", "code": "USD"}}, "to": "Счет 1111"}]',
)
def test_main_sort_ascending(mock_open_func, capsys, monkeypatch):
    inputs = iter(["1", "EXECUTED", "да", "по возрастанию", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "08.12.2019" in captured.out
    assert "15.01.2020" in captured.out
    # По возрастанию: 08.12.2019 должно быть раньше 15.01.2020
    assert captured.out.index("08.12.2019") < captured.out.index("15.01.2020")


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"id": 1, "state": "EXECUTED", "date": "2019-12-08T22:35:35", '
    '"description": "Открытие вклада", "operationAmount": {"amount": "40542", '
    '"currency": {"name": "руб.", "code": "RUB"}}, "to": "Счет 6543210987654321"},'
    '{"id": 2, "state": "EXECUTED", "date": "2020-01-15T10:00:00", '
    '"description": "Перевод", "operationAmount": {"amount": "100", '
    '"currency": {"name": "USD", "code": "USD"}}, "to": "Счет 1111"}]',
)
def test_main_ruble_only(mock_open_func, capsys, monkeypatch):
    inputs = iter(["1", "EXECUTED", "нет", "да", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Открытие вклада" in captured.out
    assert "Перевод" not in captured.out
    assert "Всего банковских операций в выборке: 1" in captured.out


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"id": 1, "state": "EXECUTED", "date": "2019-12-08T22:35:35", '
    '"description": "Открытие вклада", "operationAmount": {"amount": "40542", '
    '"currency": {"name": "руб.", "code": "RUB"}}, "to": "Счет 6543210987654321"},'
    '{"id": 2, "state": "EXECUTED", "date": "2020-01-15T10:00:00", '
    '"description": "Перевод организации", "operationAmount": {"amount": "100", '
    '"currency": {"name": "руб.", "code": "RUB"}}, "to": "Счет 1111"}]',
)
def test_main_search_filter(mock_open_func, capsys, monkeypatch):
    inputs = iter(["1", "EXECUTED", "нет", "нет", "да", "перевод"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Перевод организации" in captured.out
    assert "Открытие вклада" not in captured.out


@patch("main.read_csv_file")
def test_main_csv(mock_read_csv, capsys, monkeypatch):
    mock_read_csv.return_value = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-12-08T22:35:35",
            "description": "Открытие вклада",
            "amount": "40542",
            "currency_name": "руб.",
            "currency_code": "RUB",
            "to": "Счет 6543210987654321",
        }
    ]
    inputs = iter(["2", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "CSV" in captured.out
    assert "Открытие вклада" in captured.out


@patch("main.read_excel_file")
def test_main_excel(mock_read_excel, capsys, monkeypatch):
    mock_read_excel.return_value = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-12-08T22:35:35",
            "description": "Открытие вклада",
            "amount": "40542",
            "currency_name": "руб.",
            "currency_code": "RUB",
            "to": "Счет 6543210987654321",
        }
    ]
    inputs = iter(["3", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "XLSX" in captured.out
    assert "Открытие вклада" in captured.out
