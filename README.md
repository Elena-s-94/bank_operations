  # Bank Operations Widget

Виджет для обработки банковских операций: фильтрация по статусу и сортировка по дате.

## Возможности

- `filter_by_state`: фильтрация транзакций по состоянию (по умолчанию `"EXECUTED"`).
- `sort_by_date`: сортировка транзакций по дате (ISO‑формат), с поддержкой отсутствующих дат.

## Установка

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/Elena-s-94/bank_operations_widget.git
   cd bank_operations_widget
   
2. Установите зависимости
   (`pip requirements.txt`)

## Модуль `generators`

Модуль предоставляет генераторы для эффективной обработки транзакций и генерации данных.

### Функции

- `filter_by_currency(transactions, currency)` — возвращает генератор транзакций с заданной валютой.  
  Пример:
  ```python
  usd_transactions = filter_by_currency(transactions, "USD")
  for _ in range(2):
      print(next(usd_transactions))
  
## Модуль `utils`

Функция `read_json_file` читает JSON-файл с транзакциями и возвращает список словарей.
При ошибке (файл не найден, пустой, не список) возвращает пустой список.

## Модуль `external_api`

Функция `convert_to_rub` конвертирует сумму транзакции в рубли.
Для USD и EUR используется Exchange Rates Data API (apilayer.com).
API-ключ хранится в файле `.env` (см. `.env.template`).
