from main import Product, Smartphone, LawnGrass


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


def test_product_add_same_class():
    a = Product("A", "Desc", 50.0, 5)
    b = Product("B", "Desc", 50.0, 5)
    assert a + b == 500.0


def test_product_add_different_class_type_error():
    s = Smartphone("iPhone", "Apple", 1000.0, 10, "A16", "15", 128, "чёрный")
    g = LawnGrass("Трава", "Газон", 500.0, 20, "Россия", "7 дней", "зелёный")
    try:
        s + g
        assert False, "Должно было сработать исключение TypeError"
    except TypeError:
        pass


def test_smartphone_initialization():
    s = Smartphone("iPhone 15", "Apple", 99999.99, 10,
                   "A16 Bionic", "iPhone 15", 128, "чёрный")
    assert s.name == "iPhone 15"
    assert s.description == "Apple"
    assert s.price == 99999.99
    assert s.quantity == 10
    assert s.efficiency == "A16 Bionic"
    assert s.model == "iPhone 15"
    assert s.memory == 128
    assert s.color == "чёрный"


def test_smartphone_is_product():
    s = Smartphone("iPhone 15", "Apple", 99999.99, 10,
                   "A16 Bionic", "iPhone 15", 128, "чёрный")
    assert isinstance(s, Product)


def test_smartphone_add():
    a = Smartphone("iPhone", "Apple", 1000.0, 10, "A16", "15", 128, "чёрный")
    b = Smartphone("Samsung", "Android", 800.0, 5, "SD8", "S24", 256, "белый")
    assert a + b == 14000.0


def test_lawngrass_initialization():
    g = LawnGrass("Трава", "Газон", 500.0, 20,
                  "Россия", "7 дней", "зелёный")
    assert g.name == "Трава"
    assert g.description == "Газон"
    assert g.price == 500.0
    assert g.quantity == 20
    assert g.country == "Россия"
    assert g.germination_period == "7 дней"
    assert g.color == "зелёный"


def test_lawngrass_is_product():
    g = LawnGrass("Трава", "Газон", 500.0, 20,
                  "Россия", "7 дней", "зелёный")
    assert isinstance(g, Product)


def test_lawngrass_add():
    a = LawnGrass("Трава1", "Газон", 500.0, 20, "Россия", "7 дней", "зелёный")
    b = LawnGrass("Трава2", "Газон", 700.0, 15, "Нидерланды", "5 дней", "тёмно-зелёный")
    assert a + b == 20500.0


def test_product_add_with_base_class_type_error():
    p = Product("Base", "Desc", 100.0, 10)
    s = Smartphone("iPhone", "Apple", 1000.0, 10, "A16", "15", 128, "чёрный")
    try:
        p + s
        assert False, "Должно было сработать исключение TypeError"
    except TypeError:
        pass
