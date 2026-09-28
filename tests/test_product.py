from main import Product


def test_product_initialization():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    assert p.name == "Laptop"
    assert p.description == "Good laptop"
    assert p.price == 999.99
    assert p.quantity == 10


def test_price_rounding():
    p = Product("Test", "Desc", price=10.12345, quantity=5)
    assert p.price == 10.12


def test_product_str():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    result = str(p)
    assert "Laptop" in result
    assert "999.99" in result
    assert "10" in result
    assert "руб." in result
    assert "в наличии" in result
    assert "шт." in result


def test_product_repr():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    repr_str = repr(p)
    assert "Product" in repr_str
    assert "Laptop" in repr_str


def test_product_price_attribute():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    assert p.price == 999.99


def test_product_quantity_attribute():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    assert p.quantity == 10
