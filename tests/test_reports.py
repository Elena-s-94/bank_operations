import os
import json
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch
from src.reports import save_report, spending_by_category, spending_by_weekday, spending_by_workday

def test_spending_by_category_basic():
    df = pd.DataFrame({
        "Дата операции": ["2024-01-10", "2024-02-01", "2024-03-01"],
        "Категория": ["Продукты", "Продукты", "Транспорт"],
        "Сумма операции": [-100, -200, -300],
    })
    res = spending_by_category(df, "Продукты", date="2024-04-01")
    assert len(res) == 2
    assert set(res["Категория"]) == {"Продукты"}


def test_spending_by_category_empty():
    df = pd.DataFrame({
        "Дата операции": [],
        "Категория": [],
        "Сумма операции": [],
    })
    res = spending_by_category(df, "Продукты")
    assert res.empty


def test_spending_by_weekday_basic():
    # Используем строки дат, чтобы pd.to_datetime и логика внутри функции работали одинаково
    dates = ["2024-01-01", "2024-01-06", "2024-01-07"]
    df = pd.DataFrame({
        "Дата операции": dates,
        "Сумма операции": [-100, -200, -300],
    })
    res = spending_by_weekday(df, date="2024-01-31")
    assert not res.empty
    assert "День недели" in res.columns
    assert "Средние траты" in res.columns


def test_spending_by_workday_basic():
    dates = ["2024-01-01", "2024-01-06", "2024-01-07"]
    df = pd.DataFrame({
        "Дата операции": dates,
        "Сумма операции": [-100, -200, -300],
    })
    res = spending_by_workday(df, date="2024-01-31")
    assert not res.empty
    assert set(res["Тип дня"]) <= {"Рабочий", "Выходной"}


@patch("os.makedirs")
def test_save_report_decorator_dataframe(makedirs_mock):
    @save_report("test_report.json")
    def func():
        return pd.DataFrame({"a": [1, 2]})

    func()
    assert os.path.exists("test_report.json")
    with open("test_report.json", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    os.remove("test_report.json")


@patch("os.makedirs")
def test_save_report_decorator_dict(makedirs_mock):
    @save_report("test_report.json")
    def func():
        return {"key": "value"}

    func()
    assert os.path.exists("test_report.json")
    with open("test_report.json", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"key": "value"}
    os.remove("test_report.json")
