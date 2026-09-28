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
    assert "Остаток:" in result
    assert "шт." in result


def test_product_repr():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    repr_str = repr(p)
    assert "Product" in repr_str
    assert "Laptop" in repr_str


def test_price_getter():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    assert p.price == 999.99


def test_price_setter_positive():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    p.price = 1500.00
    assert p.price == 1500.0


def test_price_setter_zero(capsys):
    p = Product("Laptop", "Good laptop", 999.99, 10)
    p.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 999.99


def test_price_setter_negative(capsys):
    p = Product("Laptop", "Good laptop", 999.99, 10)
    p.price = -50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 999.99


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


def test_product_add():
    a = Product("Товар A", "Описание A", 100.0, 10)
    b = Product("Товар B", "Описание B", 200.0, 2)
    assert a + b == 1400.0


def test_product_add_same_prices():
    a = Product("Товар A", "Описание A", 50.0, 5)
    b = Product("Товар B", "Описание B", 50.0, 5)
    assert a + b == 500.0


def test_product_add_type_error():
    a = Product("Товар A", "Описание A", 100.0, 10)
    try:
        a + 100
        assert False, "Должно было сработать исключение TypeError"
    except TypeError:
        pass
