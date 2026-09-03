"""Модуль отчётов с декоратором для сохранения результатов в файл."""

import functools
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def save_report(filepath: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата функции-отчёта в файл.

    Args:
        filepath (Optional[str]): путь к файлу. Если None,
            используется имя по умолчанию 'reports/report.json'.

    Returns:
        Callable: декоратор.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            save_path = filepath or os.path.join("reports", "report.json")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            if isinstance(result, pd.DataFrame):
                result.to_json(save_path, orient="records", force_ascii=False, indent=2)
            else:
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

            logger.info("Отчёт сохранён в %s", save_path)
            return result

        return wrapper

    return decorator


def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца.

    Args:
        transactions (pd.DataFrame): датафрейм с транзакциями.
        category (str): название категории.
        date (Optional[str]): дата в формате 'YYYY-MM-DD'.
            Если None — берётся текущая дата.

    Returns:
        pd.DataFrame: отфильтрованный датафрейм с тратами по категории.
    """
    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

    mask = (
        (df["Категория"] == category)
        & (df["Дата операции"] >= start_date)
        & (df["Дата операции"] <= end_date)
        & (df["Сумма операции"] < 0)
    )
    return df[mask].copy()


def spending_by_weekday(
    transactions: pd.DataFrame,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """Возвращает средние траты по дням недели за последние три месяца.

    Args:
        transactions (pd.DataFrame): датафрейм с транзакциями.
        date (Optional[str]): дата в формате 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: средние траты по дням недели.
    """
    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    df = df[df["Сумма операции"] < 0].copy()
    df["abs_amount"] = df["Сумма операции"].abs()
    df["weekday"] = df["Дата операции"].dt.day_name()

    result = df.groupby("weekday")["abs_amount"].mean().round(2).reset_index()
    result.columns = ["День недели", "Средние траты"]
    return result


def spending_by_workday(
    transactions: pd.DataFrame,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """Возвращает средние траты в рабочий и выходной день за последние три месяца.

    Args:
        transactions (pd.DataFrame): датафрейм с транзакциями.
        date (Optional[str]): дата в формате 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: средние траты по типу дня (рабочий/выходной).
    """
    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    df = df[df["Сумма операции"] < 0].copy()
    df["abs_amount"] = df["Сумма операции"].abs()

    # 5 (сб) и 6 (вс) — выходные
    df["day_type"] = df["Дата операции"].dt.dayofweek.apply(lambda x: "Выходной" if x >= 5 else "Рабочий")

    result = df.groupby("day_type")["abs_amount"].mean().round(2).reset_index()
    result.columns = ["Тип дня", "Средние траты"]
    return result
