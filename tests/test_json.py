import json

from main import Product, load_categories_from_json


def test_load_categories_from_json(tmp_path):
    data = [
        {
            "name": "Тестовая категория",
            "description": "Описание",
            "products": [
                {"name": "Товар1", "description": "Описание1", "price": 100.0, "quantity": 5},
                {"name": "Товар2", "description": "Описание2", "price": 200.0, "quantity": 10},
            ],
        }
    ]
    file_path = tmp_path / "test_products.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(str(file_path))

    assert len(categories) == 1
    assert categories[0].name == "Тестовая категория"
    assert len(categories[0].products) == 2
    assert isinstance(categories[0].products[0], Product)
    assert categories[0].products[0].name == "Товар1"
    assert categories[0].products[1].price == 200.0
