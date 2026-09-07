"""Модуль для генерации JSON-ответов для веб-страниц."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from src.external_api import get_currency_rates, get_stock_prices

logger = logging.getLogger(__name__)


def get_greeting(current_time: Optional[str] = None) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    if current_time:
        hour = int(current_time.split(":")[0])
    else:
        hour = datetime.now().hour

    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает информацию по каждой карте."""
    # Явная аннотация типа для локальной переменной
    cards: List[Dict[str, Any]] = []

    if transactions.empty:
        return cards

    for card_number, group in transactions.groupby("Номер карты", dropna=False):
        if pd.isna(card_number) or not str(card_number).strip():
            continue
        last_digits = str(card_number)[-4:] if card_number else ""
        spent = group.loc[group["Сумма операции"] < 0, "Сумма операции"].sum()
        total_spent = abs(round(float(spent), 2))
        cashback = round(total_spent / 100, 2)
        cards.append(
            {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback,
            }
        )
    return cards


def get_top_transactions(transactions: pd.DataFrame, n: int = 5) -> List[Dict[str, Any]]:
    """Возвращает топ-N транзакций по сумме платежа."""
    result: List[Dict[str, Any]] = []

    if transactions.empty:
        return result

    df = transactions.copy()
    df["abs_amount"] = df["Сумма платежа"].abs()
    top = df.nlargest(n, "abs_amount")

    for _, row in top.iterrows():
        date_raw = row.get("Дата операции", "")
        if isinstance(date_raw, str):
            try:
                date_obj = datetime.strptime(date_raw, "%Y-%m-%d %H:%M:%S")
                date_str = date_obj.strftime("%d.%m.%Y")
            except ValueError:
                date_str = date_raw
        elif isinstance(date_raw, (datetime, pd.Timestamp)):
            date_str = date_raw.strftime("%d.%m.%Y")
        else:
            date_str = str(date_raw)

        result.append(
            {
                "date": date_str,
                "amount": round(float(row.get("Сумма платежа", 0)), 2),
                "category": str(row.get("Категория", "")),
                "description": str(row.get("Описание", "")),
            }
        )
    return result


def load_user_settings(filepath: str = "user_settings.json") -> Dict[str, List[str]]:
    """Загружает пользовательские настройки из JSON-файла."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Гарантируем правильный тип возврата
            return {
                "user_currencies": data.get("user_currencies", []),
                "user_stocks": data.get("user_stocks", []),
            }
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error("Ошибка загрузки настроек: %s", e)
        return {"user_currencies": [], "user_stocks": []}


def main(
    date_str: str,
    transactions: pd.DataFrame,
    user_settings_path: str = "user_settings.json",
) -> Dict[str, Any]:
    """Главная функция для страницы «Главная»."""
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.error("Неверный формат даты: %s", date_str)
        input_date = datetime.now()

    month_start = input_date.replace(day=1, hour=0, minute=0, second=0)

    # Аннотации для локальных переменных
    filtered: pd.DataFrame = transactions
    if not transactions.empty:
        df = transactions.copy()
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
        mask = (df["Дата операции"] >= month_start) & (df["Дата операции"] <= input_date)
        filtered = df[mask]

    settings: Dict[str, List[str]] = load_user_settings(user_settings_path)
    time_part = date_str.split(" ")[1] if " " in date_str else None
    greeting: str = get_greeting(time_part)

    cards: List[Dict[str, Any]] = get_cards_info(filtered)
    top_transactions: List[Dict[str, Any]] = get_top_transactions(filtered, 5)
    currency_rates: Any = get_currency_rates(settings.get("user_currencies", []))
    stock_prices: Any = get_stock_prices(settings.get("user_stocks", []))

    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }


def events(
    date_str: str,
    transactions: pd.DataFrame,
    period: str = "M",
    user_settings_path: str = "user_settings.path",
) -> Dict[str, Any]:
    """Функция для страницы «События»."""
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        input_date = datetime.now()

    filtered: pd.DataFrame = transactions
    if not transactions.empty:
        df = transactions.copy()
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

        if period == "W":
            start = input_date - pd.Timedelta(days=7)
        elif period == "M":
            start = input_date.replace(day=1, hour=0, minute=0, second=0)
        elif period == "Y":
            start = input_date.replace(month=1, day=1, hour=0, minute=0, second=0)
        else:  # ALL
            start = pd.Timestamp.min

        mask = (df["Дата операции"] >= start) & (df["Дата операции"] <= input_date)
        filtered = df[mask]

    expenses: Dict[str, Any] = _get_expenses(filtered)
    income: Dict[str, Any] = _get_income(filtered)

    settings: Dict[str, List[str]] = load_user_settings(user_settings_path)
    currency_rates: Any = get_currency_rates(settings.get("user_currencies", []))
    stock_prices: Any = get_stock_prices(settings.get("user_stocks", []))

    return {
        "expenses": expenses,
        "income": income,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }


def _get_expenses(transactions: pd.DataFrame) -> Dict[str, Any]:
    """Формирует блок расходов: основные категории и переводы/наличные."""
    if transactions.empty:
        return {"total_amount": 0, "main": [], "transfers_and_cash": []}

    df = transactions.copy()
    expenses_df = df[df["Сумма операции"] < 0]
    expenses_df = expenses_df.copy()
    expenses_df["abs_amount"] = expenses_df["Сумма операции"].abs()

    total: int = int(round(expenses_df["abs_amount"].sum()))

    transfer_categories = ["Наличные", "Переводы"]
    main_df = expenses_df[~expenses_df["Категория"].isin(transfer_categories)]
    transfer_df = expenses_df[expenses_df["Категория"].isin(transfer_categories)]

    by_category = main_df.groupby("Категория")["abs_amount"].sum().sort_values(ascending=False)
    top7 = by_category.head(7).round().astype(int).to_dict()
    rest = int(round(by_category.iloc[7:].sum())) if len(by_category) > 7 else 0

    main_list: List[Dict[str, Any]] = [{"category": str(cat), "amount": int(amt)} for cat, amt in top7.items()]
    if rest > 0:
        main_list.append({"category": "Остальное", "amount": rest})

    transfers_list = (
        transfer_df.groupby("Категория")["abs_amount"].sum().sort_values(ascending=False).round().astype(int).to_dict()
    )
    transfers_and_cash: List[Dict[str, Any]] = [
        {"category": str(cat), "amount": int(amt)} for cat, amt in transfers_list.items()
    ]

    return {
        "total_amount": total,
        "main": main_list,
        "transfers_and_cash": transfers_and_cash,
    }


def _get_income(transactions: pd.DataFrame) -> Dict[str, Any]:
    """Формирует блок поступлений."""
    if transactions.empty:
        return {"total_amount": 0, "main": []}

    df = transactions.copy()
    income_df = df[df["Сумма операции"] > 0]

    total: int = int(round(income_df["Сумма операции"].sum()))

    by_category = income_df.groupby("Категория")["Сумма операции"].sum().sort_values(ascending=False)

    main_list: List[Dict[str, Any]] = [
        {"category": str(cat), "amount": int(round(amt))} for cat, amt in by_category.items()
    ]

    return {"total_amount": total, "main": main_list}
