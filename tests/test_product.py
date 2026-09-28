import pytest

from main import BaseProduct, LawnGrass, Product, Smartphone


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
    with pytest.raises(TypeError):
        a + 100


# --- Тесты BaseProduct ---

def test_base_product_cannot_instantiate():
    with pytest.raises(TypeError):
        BaseProduct("Test", "Desc", 100.0, 5)


# --- Тесты Smartphone ---

def test_smartphone_initialization():
    s = Smartphone("iPhone", "Apple smartphone", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    assert s.name == "iPhone"
    assert s.price == 79999.0
    assert s.quantity == 5
    assert s.performance == 8.5
    assert s.model == "15 Pro"
    assert s.memory_capacity == 256
    assert s.color == "black"


def test_smartphone_inherits_product():
    s = Smartphone("iPhone", "Apple smartphone", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    assert isinstance(s, Product)
    assert isinstance(s, BaseProduct)


def test_smartphone_str():
    s = Smartphone("iPhone", "Apple smartphone", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    result = str(s)
    assert "iPhone" in result
    assert "79999" in result
    assert "руб." in result


def test_smartphone_repr():
    s = Smartphone("iPhone", "Apple smartphone", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    repr_str = repr(s)
    assert "Smartphone" in repr_str
    assert "iPhone" in repr_str
    assert "15 Pro" in repr_str
    assert "256" in repr_str


def test_smartphone_add():
    s1 = Smartphone("iPhone", "Apple", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    s2 = Smartphone("Samsung", "Android", 69999.0, 3, 9.0, "S24", 512, "white")
    result = s1 + s2
    assert result == 79999.0 * 5 + 69999.0 * 3


def test_smartphone_add_with_product():
    s = Smartphone("iPhone", "Apple", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    p = Product("Mouse", "Wireless", 29.90, 50)
    result = s + p
    assert result == 79999.0 * 5 + 29.90 * 50


def test_smartphone_price_setter():
    s = Smartphone("iPhone", "Apple", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    s.price = 89999.0
    assert s.price == 89999.0


# --- Тесты LawnGrass ---

def test_lawngrass_initialization():
    g = LawnGrass("Газон", "Зелёная трава", 500.0, 100, "Россия", "2 недели", "зелёный")
    assert g.name == "Газон"
    assert g.price == 500.0
    assert g.quantity == 100
    assert g.country == "Россия"
    assert g.germination_period == "2 недели"
    assert g.color == "зелёный"


def test_lawngrass_inherits_product():
    g = LawnGrass("Газон", "Зелёная трава", 500.0, 100, "Россия", "2 недели", "зелёный")
    assert isinstance(g, Product)
    assert isinstance(g, BaseProduct)


def test_lawngrass_str():
    g = LawnGrass("Газон", "Зелёная трава", 500.0, 100, "Россия", "2 недели", "зелёный")
    result = str(g)
    assert "Газон" in result
    assert "500" in result
    assert "руб." in result


def test_lawngrass_repr():
    g = LawnGrass("Газон", "Зелёная трава", 500.0, 100, "Россия", "2 недели", "зелёный")
    repr_str = repr(g)
    assert "LawnGrass" in repr_str
    assert "Газон" in repr_str
    assert "Россия" in repr_str


def test_lawngrass_add():
    g1 = LawnGrass("Газон", "Трава", 500.0, 100, "Россия", "2 недели", "зелёный")
    g2 = LawnGrass("Газон2", "Трава", 300.0, 50, "Беларусь", "3 недели", "тёмный")
    result = g1 + g2
    assert result == 500.0 * 100 + 300.0 * 50


# --- Тесты миксина ---

def test_mixin_prints_on_creation(capsys):
    Product("Test", "Desc", 100.0, 5)
    captured = capsys.readouterr()
    assert "Product" in captured.out
    assert "Test" in captured.out


def test_mixin_prints_smartphone(capsys):
    Smartphone("iPhone", "Apple", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    captured = capsys.readouterr()
    assert "Smartphone" in captured.out
    assert "iPhone" in captured.out


def test_mixin_prints_lawngrass(capsys):
    LawnGrass("Газон", "Трава", 500.0, 100, "Россия", "2 недели", "зелёный")
    captured = capsys.readouterr()
    assert "LawnGrass" in captured.out
    assert "Газон" in captured.out
