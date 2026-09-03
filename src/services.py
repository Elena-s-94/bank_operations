"""Модуль сервисов: поиск, телефонные номера, выгодные категории кешбэка."""

import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


def simple_search(transactions: pd.DataFrame, query: str) -> str:
    """Простой поиск транзакций по подстроке в описании или категории.

    Поиск нечувствителен к регистру.

    Args:
        transactions (pd.DataFrame): датафрейм с транзакциями.
        query (str): строка для поиска.

    Returns:
        str: JSON-строка со всеми найденными транзакциями.
    """
    if transactions.empty or not query:
        return json.dumps([], ensure_ascii=False)

    query_lower = query.lower()
    mask = transactions.apply(
        lambda row: query_lower in str(row.get("Описание", "")).lower()
        or query_lower in str(row.get("Категория", "")).lower(),
        axis=1,
    )
    result = transactions[mask].to_dict(orient="records")
    return json.dumps(result, ensure_ascii=False, default=str)


def find_phone_transactions(transactions: pd.DataFrame) -> str:
    """Поиск транзакций, содержащих мобильные номера в описании.

    Args:
        transactions (pd.DataFrame): датафрейм с транзакциями.

    Returns:
        str: JSON-строка со всеми транзакциями с телефонными номерами.
    """
    if transactions.empty:
        return json.dumps([], ensure_ascii=False)

    # Шаблоны телефонных номеров
    phone_patterns = [
        r"\+7\s?\d{3}\s?\d{2}[-\s]?\d{2}[-\s]?\d{2}",
        r"\+7\s?\d{3}\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}",
        r"8\d{10}",
        r"8\s?\d{3}\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}",
        r"\+7$\d{3}$\d{3}-\d{2}-\d{2}",
    ]
    combined = re.compile("|".join(phone_patterns))

    mask = transactions["Описание"].astype(str).apply(lambda x: bool(combined.search(x)))
    result = transactions[mask].to_dict(orient="records")
    return json.dumps(result, ensure_ascii=False, default=str)


def find_person_transfers(transactions: pd.DataFrame) -> str:
    """Поиск переводов физическим лицам.

    Категория — 'Переводы', в описании есть имя и первая буква фамилии с точкой.

    Args:
        transactions (pd.DataFrame): датафрейм с транзакциями.

    Returns:
        str: JSON-строка со всеми подходящими транзакциями.
    """
    if transactions.empty:
        return json.dumps([], ensure_ascii=False)

    # Категория "Переводы" и в описании есть "Имя Ф." (имя + пробел + заглавная буква + точка)
    name_pattern = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")
    mask = transactions.apply(
        lambda row: str(row.get("Категория", "")) == "Переводы"
        and bool(name_pattern.search(str(row.get("Описание", "")))),
        axis=1,
    )
    result = transactions[mask].to_dict(orient="records")
    return json.dumps(result, ensure_ascii=False, default=str)


def profitable_categories(transactions: pd.DataFrame, year: int, month: int) -> str:
    """Анализ выгодных категорий повышенного кешбэка.

    Args:
        transactions (pd.DataFrame): датафрейм с транзакциями.
        year (int): год для анализа.
        month (int): месяц для анализа.

    Returns:
        str: JSON с суммами кешбэка по каждой категории.
    """
    if transactions.empty:
        return json.dumps({}, ensure_ascii=False)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
    df = df[
        (df["Дата операции"].dt.year == year)
        & (df["Дата операции"].dt.month == month)
        & (df["Сумма операции"] < 0)  # только траты
    ]

    if df.empty:
        return json.dumps({}, ensure_ascii=False)

    df["abs_amount"] = df["Сумма операции"].abs()
    # Кешбэк 1% от суммы трат
    cashback = (df.groupby("Категория")["abs_amount"].sum() * 0.01).round(2).to_dict()
    return json.dumps(cashback, ensure_ascii=False)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Расчёт суммы для «Инвесткопилки».

    Округляет суммы трат до ближайшего кратного limit и возвращает
    разницу между округлённой и фактической суммой.

    Args:
        month (str): месяц в формате 'YYYY-MM'.
        transactions (List[Dict[str, Any]]): список транзакций.
        limit (int): шаг округления (10, 50, 100).

    Returns:
        float: сумма, которую удалось отложить.
    """
    total = 0.0
    for t in transactions:
        date_raw = t.get("Дата операции", "")
        amount = t.get("Сумма операции", 0)

        # Проверяем, что транзакция в нужном месяце и это трата
        try:
            date_obj = datetime.strptime(date_raw, "%Y-%m-%d")
            if date_obj.strftime("%Y-%m") != month:
                continue
        except (ValueError, TypeError):
            continue

        if amount >= 0:
            continue

        abs_amount = abs(amount)
        rounded = ((int(abs_amount) // limit) + 1) * limit
        total += rounded - abs_amount

    return round(total, 2)
