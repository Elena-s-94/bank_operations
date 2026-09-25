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


def test_price_getter(sample_product):
    assert sample_product.price == 999.99


def test_price_setter_positive(sample_product):
    sample_product.price = 1500.00
    assert sample_product.price == 1500.0


def test_price_setter_zero(sample_product, capsys):
    sample_product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 999.99


def test_price_setter_negative(sample_product, capsys):
    sample_product.price = -50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 999.99


def test_new_product_from_dict():
    data = {"name": "Phone", "description": "Smartphone", "price": 500.0, "quantity": 30}
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "Phone"
    assert p.price == 500.0
    assert p.quantity == 30


def test_new_product_duplicate():
    existing = Product("Phone", "Smartphone", 500.0, 30)
    data = {"name": "Phone", "description": "Smartphone", "price": 600.0, "quantity": 20}
    result = Product.new_product(data, products_list=[existing])
    assert result is existing
    assert result.quantity == 50
    assert result.price == 600.0
