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
  
## Наследование и проверка типов

Созданы классы-наследники `Product`:
- `Smartphone` — расширен атрибутами: `efficiency`, `model`, `memory`, `color`.
- `LawnGrass` — расширен атрибутами: `country`, `germination_period`, `color`.

Реализованы ограничения:
- `__add__`: складывать можно только товары одного класса (проверка через `type()`).
- `add_product()`: в категорию можно добавлять только `Product` и его наследников (проверка через `isinstance()`).
