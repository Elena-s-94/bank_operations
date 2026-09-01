import logging
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger("read_csv_xlsx")
file_handler = logging.FileHandler("logs/read_csv_xlsx.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Принимает путь к CSV-файлу и возвращает список словарей с транзакциями.
    Разделитель — точка с запятой (;). При ошибке возвращает пустой список.

    Args:
        file_path (str): путь к CSV-файлу.

    Returns:
        List[Dict[str, Any]]: список словарей с транзакциями.
    """
    try:
        df = pd.read_csv(file_path, sep=";")
        transactions = df.to_dict(orient="records")
        logger.info("CSV-файл %s прочитан, найдено %d записей", file_path, len(transactions))
        return transactions
    except FileNotFoundError:
        logger.error("CSV-файл %s не найден", file_path)
        return []
    except Exception as e:
        logger.error("Ошибка при чтении CSV-файла %s: %s", file_path, e)
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (.xlsx).

    Принимает путь к Excel-файлу и возвращает список словарей с транзакциями.
    При ошибке возвращает пустой список.

    Args:
        file_path (str): путь к Excel-файлу.

    Returns:
        List[Dict[str, Any]]: список словарей с транзакциями.
    """
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        logger.info("Excel-файл %s прочитан, найдено %d записей", file_path, len(transactions))
        return transactions
    except FileNotFoundError:
        logger.error("Excel-файл %s не найден", file_path)
        return []
    except Exception as e:
        logger.error("Ошибка при чтении Excel-файла %s: %s", file_path, e)
        return []
