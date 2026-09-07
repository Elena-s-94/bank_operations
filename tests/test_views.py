import pandas as pd
from src.views import main, get_cards_info


def test_get_cards_info_returns_correct_data():
    df = pd.DataFrame({
        "Номер карты": ["*4556", "*5091", "*4556"],
        "Сумма операции": [-1000, -2000, -500],
    })
    cards = get_cards_info(df)
    assert len(cards) == 2
    assert any(c["last_digits"] == "4556" for c in cards)
    assert any(c["last_digits"] == "5091" for c in cards)


def test_main_returns_expected_keys():
    df = pd.DataFrame({
        "Дата операции": ["2021-12-30 10:00:00", "2021-12-31 12:00:00"],
        "Номер карты": ["*4556", "*5091"],
        "Сумма операции": [-1000, 2000],
        "Сумма платежа": [-1000, 2000],
        "Категория": ["Продукты", "Пополнения"],
        "Описание": ["Покупка в магазине", "Перевод себе"],
    })
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])

    result = main("2021-12-31 23:59:59", df)

    assert isinstance(result, dict)
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result

import pandas as pd
from src.views import (
    main,
    get_cards_info,
    get_greeting,
    get_top_transactions,
    load_user_settings,
    events,
)


def test_get_greeting_morning():
    assert get_greeting("08:00:00") == "Доброе утро"


def test_get_greeting_day():
    assert get_greeting("13:00:00") == "Добрый день"


def test_get_greeting_evening():
    assert get_greeting("19:00:00") == "Добрый вечер"


def test_get_greeting_night():
    assert get_greeting("23:59:00") == "Доброй ночи"


def test_get_greeting_no_args():
    """Покрывает ветку с datetime.now().hour"""
    result = get_greeting()
    assert result in ("Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи")


def test_get_top_transactions_with_data():
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2021-12-30 10:00:00", "2021-12-31 12:00:00"]),
        "Сумма платежа": [-500, -1500],
        "Категория": ["Продукты", "Бензин"],
        "Описание": ["Пятёрочка", "Лукойл"],
    })
    result = get_top_transactions(df, 5)
    assert len(result) == 2
    assert result[0]["amount"] == -1500  # наибольшая по модулю — первая
    assert result[0]["category"] == "Бензин"


def test_get_top_transactions_empty():
    df = pd.DataFrame()
    result = get_top_transactions(df, 5)
    assert result == []


def test_load_user_settings_success(tmp_path):
    import json
    settings_file = tmp_path / "settings.json"
    settings_file.write_text(json.dumps({"user_currencies": ["USD"], "user_stocks": ["AAPL"]}), encoding="utf-8")
    result = load_user_settings(str(settings_file))
    assert result["user_currencies"] == ["USD"]
    assert result["user_stocks"] == ["AAPL"]


def test_load_user_settings_file_not_found():
    result = load_user_settings("несуществующий_файл.json")
    assert result == {"user_currencies": [], "user_stocks": []}


def test_events_returns_expected_keys():
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2021-12-15 10:00:00", "2021-12-20 12:00:00"]),
        "Сумма операции": [-1000, 2000],
        "Категория": ["Продукты", "Пополнения"],
    })
    result = events("2021-12-31 23:59:59", df, period="M")
    assert "expenses" in result
    assert "income" in result
    assert "currency_rates" in result
    assert "stock_prices" in result


def test_get_cards_info_empty():
    df = pd.DataFrame()
    result = get_cards_info(df)
    assert result == []
