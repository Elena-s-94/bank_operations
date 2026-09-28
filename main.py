import json
from abc import ABC, abstractmethod


class ZeroQuantityError(ValueError):
    """Исключение для товара с нулевым количеством."""


class ProductReprMixin:
    """Миксин, печатающий информацию о создании объекта."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(repr(self))


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов магазина."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = round(price, 2)
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой положительного значения."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self._price = round(new_price, 2)

    @classmethod
    def new_product(cls, product_data: dict, products_list: list | None = None) -> "BaseProduct":
        """Создаёт объект из словаря. Если товар с таким именем уже
        существует — складывает количество и выбирает более высокую цену."""
        name = product_data["name"]

        if products_list:
            for existing in products_list:
                if existing.name == name:
                    existing.quantity += product_data["quantity"]
                    if product_data["price"] > existing.price:
                        existing.price = product_data["price"]
                    return existing

        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __add__(self, other: "BaseProduct") -> float:
        """Сложение двух товаров: возвращает сумму произведений цены на количество."""
        if not isinstance(other, BaseProduct):
            raise TypeError("Можно складывать только объекты класса Product")
        return self.price * self.quantity + other.price * other.quantity

    def __str__(self) -> str:
        """Строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(name={self.name!r}, description={self.description!r}, "
            f"price={self.price}, quantity={self.quantity})"
        )


class Product(ProductReprMixin, BaseProduct):
    """Класс для описания товара в интернет-магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name, description, price, quantity)


class Smartphone(Product):
    """Класс для описания смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        performance: float,
        model: str,
        memory_capacity: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.performance = performance
        self.model = model
        self.memory_capacity = memory_capacity
        self.color = color

    def __repr__(self) -> str:
        return (
            f"Smartphone(name={self.name!r}, description={self.description!r}, "
            f"price={self.price}, quantity={self.quantity}, "
            f"performance={getattr(self, 'performance', 'N/A')}, "
            f"model={getattr(self, 'model', 'N/A')!r}, "
            f"memory_capacity={getattr(self, 'memory_capacity', 'N/A')}, "
            f"color={getattr(self, 'color', 'N/A')!r})"
        )


class LawnGrass(Product):
    """Класс для описания травы газонной."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self) -> str:
        return (
            f"LawnGrass(name={self.name!r}, description={self.description!r}, "
            f"price={self.price}, quantity={self.quantity}, "
            f"country={getattr(self, 'country', 'N/A')!r}, "
            f"germination_period={getattr(self, 'germination_period', 'N/A')!r}, "
            f"color={getattr(self, 'color', 'N/A')!r})"
        )


class BaseCategoryOrder(ABC):
    """Абстрактный базовый класс для категорий и заказов."""

    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def total_cost(self) -> float:
        """Общая стоимость всех товаров."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Category(BaseCategoryOrder):
    """Класс для описания категории товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[BaseProduct] | None = None,
    ):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: BaseProduct) -> None:
        """Добавляет продукт в категорию с обработкой нулевого количества."""
        try:
            if product.quantity == 0:
                raise ZeroQuantityError(
                    "Товар с нулевым количеством не может быть добавлен"
                )
            self.__products.append(product)
            Category.product_count += 1
        except ZeroQuantityError as e:
            print(e)
        else:
            print("Товар успешно добавлен")
        finally:
            print("Обработка добавления товара завершена")

    @property
    def products(self) -> str:
        """Геттер, возвращающий список товаров в виде отформатированной строки."""
        result = ""
        for product in self.__products:
            result += f"{product}\n"
        return result

    @property
    def total_cost(self) -> float:
        """Общая стоимость всех товаров в категории."""
        return sum(p.price * p.quantity for p in self.__products)

    def average_price(self) -> float:
        """Подсчитывает средний ценник всех товаров категории."""
        try:
            return sum(p.price for p in self.__products) / len(self.__products)
        except ZeroDivisionError:
            return 0

    def __str__(self) -> str:
        """Строковое представление категории."""
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __repr__(self) -> str:
        return (
            f"Category(name={self.name!r}, description={self.description!r}, "
            f"products={self.__products!r})"
        )


class Order(BaseCategoryOrder):
    """Класс для описания заказа."""

    def __init__(self, product: BaseProduct, quantity: int):
        if not isinstance(product, BaseProduct):
            raise TypeError("Товар должен быть объектом класса Product")
        if quantity == 0:
            raise ZeroQuantityError("Товар с нулевым количеством не может быть добавлен")
        if quantity < 0:
            raise ValueError("Количество должно быть положительным")
        self.product = product
        self.quantity = quantity

    @property
    def total_cost(self) -> float:
        """Итоговая стоимость заказа."""
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"Заказ: {self.product.name}, {self.quantity} шт., итого: {self.total_cost} руб."

    def __repr__(self) -> str:
        return f"Order(product={self.product!r}, quantity={self.quantity})"


def load_categories_from_json(path: str) -> list[Category]:
    """Загружает категории и товары из JSON-файла."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    categories: list[Category] = []
    for item in data:
        products = [
            Product(
                name=p["name"],
                description=p["description"],
                price=p["price"],
                quantity=p["quantity"],
            )
            for p in item.get("products", [])
        ]
        category = Category(
            name=item["name"],
            description=item["description"],
            products=products,
        )
        categories.append(category)
    return categories


if __name__ == "__main__":
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
    c = Category("Electronics", "All electronics", [p1, p2])
    print(c)
    print(c.products)

    p3 = Product.new_product(
        {"name": "Keyboard", "description": "Mechanical", "price": 1500.0, "quantity": 20}
    )
    c.add_product(p3)
    print(c.products)
    print(f"Категорий: {Category.category_count}, Товаров: {Category.product_count}")

    print(f"Сложение товаров: {p1 + p2}")
    print(f"Сумма Laptop и Keyboard: {p1 + p3}")

    s = Smartphone("iPhone", "Apple smartphone", 79999.0, 5, 8.5, "15 Pro", 256, "black")
    g = LawnGrass("Газон", "Зелёная трава", 500.0, 100, "Россия", "2 недели", "зелёный")
    print(s)
    print(g)
    print(f"Сложение Smartphone и LawnGrass: {s + g}")

    order = Order(p1, 3)
    print(order)
    print(f"Общая стоимость категории: {c.total_cost} руб.")
    print(f"Средний ценник категории: {c.average_price()} руб.")

    # Демонстрация обработки нулевого количества
    try:
        Product("Zero", "Test", 100.0, 0)
    except ValueError as e:
        print(f"Ошибка: {e}")

    empty_cat = Category("Empty", "No products", None)
    print(f"Средний ценник пустой категории: {empty_cat.average_price()}")
