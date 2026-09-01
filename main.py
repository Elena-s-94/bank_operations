import json
import os

from src.masks import get_mask_account
from src.processing import process_bank_search
from src.read_csv_xlsx import read_csv_file, read_excel_file
from src.widget import get_date


def get_amount_and_currency(transaction: dict) -> tuple[str, str]:
    """Извлекает сумму и валюту из транзакции (поддерживает JSON и CSV/XLSX)."""
    if "operationAmount" in transaction:
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["name"]
    else:
        amount = str(transaction.get("amount", ""))
        currency = transaction.get("currency_name", transaction.get("currency", ""))
    return amount, currency


def get_currency_code(transaction: dict) -> str:
    """Извлекает код валюты из транзакции (поддерживает JSON и CSV/XLSX)."""
    if "operationAmount" in transaction:
        return transaction["operationAmount"]["currency"]["code"]
    return str(transaction.get("currency_code", transaction.get("currency", "")))


def format_transaction(transaction: dict) -> str:
    """Форматирует транзакцию для вывода в консоль."""
    date = get_date(transaction.get("date", ""))
    description = transaction.get("description", "")
    amount, currency = get_amount_and_currency(transaction)

    from_field = transaction.get("from", "")
    to_field = transaction.get("to", "")

    from_masked = get_mask_account(from_field) if from_field else ""
    to_masked = get_mask_account(to_field) if to_field else ""

    if from_masked and to_masked:
        second_line = f"{from_masked} -> {to_masked}"
    elif to_masked:
        second_line = to_masked
    else:
        second_line = ""

    return f"{date} {description}\n{second_line}\nСумма: {amount} {currency}"


def main() -> None:
    """Основная логика проекта. Связывает функциональности между собой."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input()

    # Чтение данных
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        json_path = "data/operations.json"
        if not os.path.exists(json_path):
            json_path = "operations.json"
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        data = read_csv_file("data/transactions.csv")
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        data = read_excel_file("data/transactions_excel.xlsx")
    else:
        print("Неверный пункт меню.")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input().upper()
        if status in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            break
        else:
            print(f'Статус операции "{status}" недоступен.')

    data = [t for t in data if t.get("state", "").upper() == status]

    # Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    sort_answer = input().lower()
    if sort_answer == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        order = input().lower()
        if "возраст" in order:
            data = sorted(data, key=lambda x: x.get("date", ""))
        else:
            data = sorted(data, key=lambda x: x.get("date", ""), reverse=True)

    # Фильтр только рублёвых
    print("Выводить только рублевые транзакции? Да/Нет")
    ruble_answer = input().lower()
    if ruble_answer == "да":
        data = [t for t in data if get_currency_code(t) == "RUB"]

    # Фильтр по слову в описании
    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_answer = input().lower()
    if search_answer == "да":
        print("Введите слово для поиска:")
        search_word = input()
        data = process_bank_search(data, search_word)

    # Вывод результата
    print("Распечатываю итоговый список транзакций...")
    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(data)}")
        for t in data:
            print()
            print(format_transaction(t))


if __name__ == "__main__":
    main()
