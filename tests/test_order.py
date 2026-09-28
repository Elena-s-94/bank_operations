import pytest

from main import BaseCategoryOrder, Category, Order, Product, Smartphone


def test_order_initialization():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    order = Order(p, 3)
    assert order.product is p
    assert order.quantity == 3
    assert order.total_cost == 999.99 * 3


def test_order_total_cost():
    p = Product("Mouse", "Wireless mouse", 29.90, 50)
    order = Order(p, 5)
    assert order.total_cost == 29.90 * 5


def test_order_str():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    order = Order(p, 3)
    result = str(order)
    assert "Заказ" in result
    assert "Laptop" in result
    assert "3" in result
    assert "руб." in result


def test_order_repr():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    order = Order(p, 3)
    repr_str = repr(order)
    assert "Order" in repr_str
    assert "3" in repr_str


def test_order_with_smartphone():
    s = Smartphone("iPhone", "Apple", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    order = Order(s, 2)
    assert order.total_cost == 79999.0 * 2
    assert "iPhone" in str(order)


def test_order_invalid_product_type():
    with pytest.raises(TypeError):
        Order("not a product", 5)


def test_order_zero_quantity():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    with pytest.raises(ValueError):
        Order(p, 0)


def test_order_negative_quantity():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    with pytest.raises(ValueError):
        Order(p, -3)


def test_base_category_order_cannot_instantiate():
    with pytest.raises(TypeError):
        BaseCategoryOrder()


def test_order_inherits_base_category_order():
    p = Product("Laptop", "Good laptop", 999.99, 10)
    order = Order(p, 3)
    assert isinstance(order, BaseCategoryOrder)


def test_category_inherits_base_category_order():
    c = Category("Test", "Desc", products=[])
    assert isinstance(c, BaseCategoryOrder)
