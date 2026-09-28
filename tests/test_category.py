from main import Category, Product


def test_category_initialization():
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
    c = Category("Electronics", "All electronics", [p1, p2])

    assert c.name == "Electronics"
    assert c.description == "All electronics"
    assert isinstance(c.products, list)
    assert len(c.products) == 2
    assert c.products[0].name == "Laptop"
    assert c.products[1].name == "Mouse"


def test_category_empty_products():
    c = Category("Empty", "No products", None)
    assert c.products == []


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


def test_category_str():
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
    c = Category("Electronics", "All electronics", [p1, p2])
    result = str(c)
    assert "Electronics" in result
    assert "2" in result
    assert "товаров" in result


def test_category_str_empty():
    c = Category("Empty", "No products", None)
    result = str(c)
    assert "Empty" in result
    assert "0" in result


def test_category_repr():
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    c = Category("Electronics", "All electronics", [p1])
    repr_str = repr(c)
    assert "Category" in repr_str
    assert "Electronics" in repr_str


def test_load_categories_from_json():
    from main import load_categories_from_json
    import os

    json_path = os.path.join(os.path.dirname(__file__), "..", "products.json")
    if os.path.exists(json_path):
        categories = load_categories_from_json(json_path)
        assert len(categories) > 0
        assert isinstance(categories[0], Category)
