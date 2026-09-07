"""Модуль для чтения данных из CSV и Excel файлов."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def read_excel_file(filepath: str) -> pd.DataFrame:
    """Читает Excel-файл (.xlsx, .xls) в DataFrame.

    Args:
        filepath (str): путь к файлу.

    Returns:
        pd.DataFrame: данные из файла.
    """
    path = Path(filepath)
    if not path.exists():
        logger.error("Файл не найден: %s", filepath)
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    try:
        df = pd.read_excel(path, engine="openpyxl")
        # Сюда вставляем преобразование даты:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="coerce")

        logger.info("Excel-файл успешно прочитан: %s (строк: %d)", filepath, len(df))
        return df
    except Exception as e:
        logger.error("Ошибка при чтении Excel-файла: %s", e)
        raise


def read_csv_file(filepath: str, encoding: str = "utf-8") -> pd.DataFrame:
    """Читает CSV-файл в DataFrame.

    Args:
        filepath (str): путь к файлу.
        encoding (str): кодировка файла.

    Returns:
        pd.DataFrame: данные из файла.
    """
    path = Path(filepath)
    if not path.exists():
        logger.error("Файл не найден: %s", filepath)
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    try:
        df = pd.read_csv(path, encoding=encoding)
        logger.info("CSV-файл успешно прочитан: %s (строк: %d)", filepath, len(df))
        return df
    except Exception as e:
        logger.error("Ошибка при чтении CSV-файла: %s", e)
        raise
