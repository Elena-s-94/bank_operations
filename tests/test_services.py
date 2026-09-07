import json
import re
import pandas as pd
from src.services import simple_search, find_phone_transactions, find_person_transfers, profitable_categories, investment_bank

def test_simple_search_found():
    df = pd.DataFrame([
        {"Описание": "Покупка в Пятёрочке", "Категория": "Продукты"},
        {"Описание": "Перевод другу", "Категория": "Переводы"},
    ])
    res_json = simple_search(df, "пят")
    res = json.loads(res_json)
    assert len(res) == 1
    assert res[0]["Категория"] == "Продукты"

def test_simple_search_not_found():
    df = pd.DataFrame([{"Описание": "Оплата ЖКХ", "Категория": "ЖКХ"}])
    res_json = simple_search(df, "пят")
    res = json.loads(res_json)
    assert res == []

def test_find_phone_transactions_found():
    df = pd.DataFrame([
        {"Описание": "Перевод +7 999 123-45-67"},
        {"Описание": "Оплата услуг"},
    ])
    res_json = find_phone_transactions(df)
    res = json.loads(res_json)
    assert len(res) == 1

def test_find_person_transfers_found():
    df = pd.DataFrame([
        {"Категория": "Переводы", "Описание": "Иванову И."},
        {"Категория": "Переводы", "Описание": "Петрову П."},
        {"Категория": "Продукты", "Описание": "Иванову И."},
    ])
    res_json = find_person_transfers(df)
    res = json.loads(res_json)
    assert len(res) == 2

def test_profitable_categories_basic():
    df = pd.DataFrame({
        "Дата операции": ["2023-05-01", "2023-05-10", "2023-06-01"],
        "Категория": ["Продукты", "Продукты", "Транспорт"],
        "Сумма операции": [-1000, -2000, -500],
    })
    res_json = profitable_categories(df, 2023, 5)
    res = json.loads(res_json)
    # 1% кешбэк: (1000+2000)*0.01 = 30
    assert res["Продукты"] == 30.0

def test_investment_bank_basic():
    transactions = [
        {"Дата операции": "2023-10-01", "Сумма операции": -123},
        {"Дата операции": "2023-10-15", "Сумма операции": -278},
    ]
    total = investment_bank("2023-10", transactions, 100)
    # 123 -> 200 (разница 77), 278 -> 300 (разница 22), итого 99
    assert total == 99.0
    