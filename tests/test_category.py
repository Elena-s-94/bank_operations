from main import Category, Product


def test_category_initialization():
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
    c = Category("Electronics", "All electronics", [p1, p2])

    assert c.name == "Electronics"
    assert c.description == "All electronics"
    assert isinstance(c.products, str)
    assert "Laptop" in c.products
    assert "Mouse" in c.products


def test_category_empty_products():
    c = Category("Empty", "No products", None)
    assert c.products == ""


def test_category_counters_on_creation():
    initial_cat = Category.category_count
    initial_prod = Category.product_count

    Category("Books", "All books", products=[])
    assert Category.category_count == initial_cat + 1
    assert Category.product_count == initial_prod

    p1 = Product("Book A", "Nice book", 15.50, 100)
    Category("Books2", "More books", products=[p1])
    assert Category.category_count == initial_cat + 2
    assert Category.product_count == initial_prod + 1


def test_category_counters_multiple_products():
    initial_prod = Category.product_count

    p1 = Product("Item1", "Desc1", 10.0, 5)
    p2 = Product("Item2", "Desc2", 20.0, 3)
    p3 = Product("Item3", "Desc3", 30.0, 1)
    Category("TestCat", "Test desc", products=[p1, p2, p3])

    assert Category.product_count == initial_prod + 3


def test_add_product():
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
    c = Category("Electronics", "All electronics", [p1, p2])
    initial_prod_count = Category.product_count

    new_p = Product("Keyboard", "Mechanical", 1500.0, 20)
    c.add_product(new_p)

    assert Category.product_count == initial_prod_count + 1
    assert "Keyboard" in c.products
    assert "1500" in c.products


def test_add_product_increments_counter():
    initial = Category.product_count
    c = Category("Test", "Test desc", products=[])
    p = Product("Item", "Desc", 10.0, 5)
    c.add_product(p)
    assert Category.product_count == initial + 1


def test_products_getter_format():
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
    c = Category("Electronics", "All electronics", [p1, p2])
    products_str = c.products
    assert "Laptop" in products_str
    assert "руб." in products_str
    assert "Остаток:" in products_str
    assert "шт." in products_str


def test_category_str():
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
    c = Category("Electronics", "All electronics", [p1, p2])
    result = str(c)
    assert "Electronics" in result
    assert "количество продуктов" in result
    assert "60" in result


def test_category_str_empty():
    c = Category("Empty", "No products", None)
    result = str(c)
    assert "Empty" in result
    assert "0" in result


def test_category_str_multiple_quantities():
    p1 = Product("A", "Desc", 10.0, 5)
    p2 = Product("B", "Desc", 20.0, 3)
    p3 = Product("C", "Desc", 30.0, 2)
    c = Category("Test", "Desc", products=[p1, p2, p3])
    result = str(c)
    assert "10" in result

    def test_average_price():
        p1 = Product("Laptop", "Good laptop", 999.99, 10)
        p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
        c = Category("Electronics", "All electronics", [p1, p2])
        expected = (999.99 + 29.90) / 2
        assert c.average_price() == expected

    def test_average_price_empty():
        c = Category("Empty", "No products", None)
        assert c.average_price() == 0

    def test_average_price_single_product():
        p = Product("Item", "Desc", 500.0, 10)
        c = Category("Single", "One product", [p])
        assert c.average_price() == 500.0

    def test_average_price_after_add():
        c = Category("Test", "Desc", products=[])
        p1 = Product("A", "Desc", 100.0, 5)
        p2 = Product("B", "Desc", 200.0, 3)
        c.add_product(p1)
        c.add_product(p2)
        assert c.average_price() == 150.0

    def test_add_product_zero_quantity_message(capsys):
        p = Product("Test", "Desc", 100.0, 5)
        p.quantity = 0
        c = Category("Test", "Desc", products=[])
        c.add_product(p)
        captured = capsys.readouterr()
        assert "Товар с нулевым количеством не может быть добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_add_product_success_message(capsys):
        p = Product("Test", "Desc", 100.0, 5)
        c = Category("Test", "Desc", products=[])
        c.add_product(p)
        captured = capsys.readouterr()
        assert "Товар успешно добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_add_product_zero_quantity_not_added(capsys):
        p = Product("Test", "Desc", 100.0, 5)
        p.quantity = 0
        c = Category("Test", "Desc", products=[])
        initial_count = Category.product_count
        c.add_product(p)
        assert Category.product_count == initial_count
        assert c.products == ""


def test_load_categories_from_json(tmp_path):
    import json
    from main import load_categories_from_json

    data = [
        {
            "name": "Electronics",
            "description": "Electronic goods",
            "products": [
                {"name": "Laptop", "description": "Good laptop", "price": 999.99, "quantity": 10},
                {"name": "Mouse", "description": "Wireless", "price": 29.90, "quantity": 50},
            ],
        },
        {
            "name": "Books",
            "description": "All books",
            "products": [],
        },
    ]
    json_file = tmp_path / "products.json"
    json_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(str(json_file))
    assert len(categories) == 2
    assert categories[0].name == "Electronics"
    assert categories[1].name == "Books"
    assert "Laptop" in categories[0].products
    assert "Mouse" in categories[0].products
    assert categories[1].products == ""
