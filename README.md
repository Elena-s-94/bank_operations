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
  
```markdown
## Модуль `decorators`

Добавлен декоратор `log`, который логирует выполнение функций.

- Если указан `filename`, логи пишутся в файл.
- Если `filename` не задан, логи выводятся в консоль.
- При успехе: `<имя_функции> ok`.
- При ошибке: `<имя_функции> error: <тип_ошибки>. Inputs: <аргументы>`.

Пример:

```python
from decorators import log

@log(filename="mylog.txt")
def add(x, y):
    return x + y

add(1, 2)
