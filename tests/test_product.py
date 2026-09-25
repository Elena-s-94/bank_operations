from main import Product


def test_product_initialization(sample_product):
    assert sample_product.name == "Laptop"
    assert sample_product.description == "Good laptop"
    assert sample_product.price == 999.99
    assert sample_product.quantity == 10


def test_price_rounding():
    p = Product("Test", "Desc", price=10.12345, quantity=5)
    assert p.price == 10.12


def test_product_str(sample_product):
    assert "Laptop" in str(sample_product)
    assert "999.99" in str(sample_product)


def test_product_repr(sample_product):
    repr_str = repr(sample_product)
    assert "Product" in repr_str
    assert "Laptop" in repr_str
