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
