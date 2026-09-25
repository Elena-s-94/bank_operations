# E-commerce Core

Ядро для интернет-магазина: классы Product и Category, счётчики, тесты.

## Реализованный функционал

- **Product** — класс товара с атрибутами: name, description, price, quantity.
- **Category** — класс категории с атрибутами: name, description, products (список объектов Product).
- **Атрибуты класса Category**: category_count и product_count — автоматически увеличиваются при создании новых объектов.
- **load_categories_from_json()** — загрузка категорий и товаров из JSON-файла.

## Запуск тестов

```bash
poetry install
poetry run pytest --cov=main --cov-report=html
