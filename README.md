# Bank Operations Widget

Виджет для обработки банковских операций: фильтрация по статусу и сортировка по дате, а также расширенный анализ транзакций (отчёты, маскирование данных, поиск).

## Возможности

Проект реализует следующие функциональные модули:

### Модуль `processing` (базовая обработка)

- `filter_by_state`: фильтрация транзакций по состоянию (по умолчанию `"EXECUTED"`).
- `sort_by_date`: сортировка транзакций по дате (ISO-формат), с поддержкой отсутствующих дат.

### Модуль `generators` (эффективная обработка данных)

- `filter_by_currency(transactions, currency)`: возвращает генератор транзакций с заданной валютой.

  Пример:
  ```python
  usd_transactions = filter_by_currency(transactions, "USD")
  for _ in range(2):
      print(next(usd_transactions))
  ```

### Модуль `reports` (аналитика и отчёты)

- `spending_by_category`: траты по категории за последние 3 месяца.
- `spending_by_weekday`: средние траты по дням недели.
- `spending_by_workday`: сравнение трат в рабочие и выходные дни.
- Декоратор `save_report`: автоматическое сохранение результатов в JSON-файл.

### Модуль `masks` (безопасность данных)

- `get_mask_card_number`: маскировка номера карты (формат `XXXX XX** **** XXXX`).
- `get_mask_account`: маскировка номера счёта (отображаются только последние 4 цифры).

### Модуль `services` (поиск и аналитика)

- `simple_search`: поиск транзакций по подстроке.
- `find_phone_transactions`: поиск операций с телефонными номерами.
- `find_person_transfers`: поиск переводов физлицам.
- `profitable_categories`: расчёт потенциального кешбэка.
- `investment_bank`: расчёт суммы для «Инвесткопилки».

---

## Установка и запуск

Проект использует **Poetry** для управления зависимостями.

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Elena-s-94/bank_operations.git
   cd bank_operations
   ```

2. Установите зависимости:
   ```bash
   poetry install
   ```

3. Запуск приложения:
   ```bash
   poetry run python src/main.py
   ```

---

## Тестирование и покрытие кода

Покрытие кода тестами — **86%** (требование проекта — не менее 80%).

Запуск тестов с отчётом о покрытии:
```bash
poetry run pytest --cov=src --cov-report=term-missing
```

Покрытие по модулям:

| Модуль | Покрытие |
| --- | --- |
| `processing.py` | 100% |
| `generators.py` | 100% |
| `widget.py` | 100% |
| `reports.py` | 97% |
| `external_api.py` | 91% |
| `views.py` | 84% |
| `services.py` | 84% |
| `read_csv_xlsx.py` | 80% |
| `masks.py` | 61% |

Тесты расположены в папке `tests/`, каждый модуль имеет соответствующий файл (`test_masks.py`, `test_reports.py` и т.д.).

---

## Структура проекта

```
src/
├── external_api.py      # запросы к API курсов валют и цен акций
├── generators/          # генераторы для обработки транзакций
├── masks.py             # маскирование номеров карт и счетов
├── processing.py        # фильтрация и сортировка
├── read_csv_xlsx.py     # чтение CSV и Excel файлов
├── reports.py           # аналитика и отчёты
├── services.py          # поиск и аналитика
├── views.py             # главная страница и события
└── widget.py            # виджет маскирования и дат

tests/
├── test_external_api.py
├── test_generators.py
├── test_masks.py
├── test_processing.py
├── test_read_csv_xlsx.py
├── test_reports.py
├── test_services.py
├── test_views.py
└── test_widget.py
```

---

## Лицензия

Проект распространяется под лицензией MIT.
