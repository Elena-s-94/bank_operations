from main import Category, Product


def test_category_initialization(sample_category, sample_product, another_product):
    assert sample_category.name == "Electronics"
    assert sample_category.description == "All electronics"
    assert isinstance(sample_category.products, str)
    assert "Laptop" in sample_category.products
    assert "Mouse" in sample_category.products


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


def test_add_product(sample_category):
    new_p = Product("Keyboard", "Mechanical", 1500.0, 20)
    initial_prod_count = Category.product_count

    sample_category.add_product(new_p)

    assert Category.product_count == initial_prod_count + 1
    assert "Keyboard" in sample_category.products
    assert "1500" in sample_category.products


def test_add_product_increments_counter():
    initial = Category.product_count
    c = Category("Test", "Test desc", products=[])
    p = Product("Item", "Desc", 10.0, 5)
    c.add_product(p)
    assert Category.product_count == initial + 1


def test_products_getter_format(sample_category):
    products_str = sample_category.products
    assert "Laptop" in products_str
    assert "руб." in products_str
    assert "Остаток:" in products_str
    assert "шт." in products_str
