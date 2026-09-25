from main import Category, Product


def test_category_initialization(sample_category, sample_product, another_product):
    assert sample_category.name == "Electronics"
    assert sample_category.description == "All electronics"
    assert len(sample_category.products) == 2
    assert sample_category.products[0] is sample_product
    assert sample_category.products[1] is another_product


def test_category_empty_products():
    c = Category("Empty", "No products", None)
    assert c.products == []


def test_category_counters_on_creation():
    initial_cat = Category.category_count
    initial_prod = Category.product_count

    # Создаём категорию без товаров — счётчик категорий должен вырасти на 1
    Category("Books", "All books", products=[])
    assert Category.category_count == initial_cat + 1
    assert Category.product_count == initial_prod

    p1 = Product("Book A", "Nice book", 15.50, 100)
    # Создаём категорию с одним товаром — счётчик категорий +1, товаров +1
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
