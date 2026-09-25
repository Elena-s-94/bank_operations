import json

from main import load_categories_from_json


def test_load_categories_from_json(tmp_path):
    data = [
        {
            "name": "Тестовая категория",
            "description": "Описание",
            "products": [
                {
                    "name": "Товар1",
                    "description": "Описание1",
                    "price": 100.0,
                    "quantity": 5,
                },
                {
                    "name": "Товар2",
                    "description": "Описание2",
                    "price": 200.0,
                    "quantity": 10,
                },
            ],
        }
    ]
    file_path = tmp_path / "test_products.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(str(file_path))

    assert len(categories) == 1
    assert categories[0].name == "Тестовая категория"
    assert isinstance(categories[0].products, str)
    assert "Товар1" in categories[0].products
    assert "Товар2" in categories[0].products
