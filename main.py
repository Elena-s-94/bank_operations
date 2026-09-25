import json


class Product:
    """Базовый класс для описания товара в интернет-магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = round(price, 2)
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, products_list: list | None = None) -> "Product":
        """Создаёт объект Product из словаря. Если товар с таким именем уже
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

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой положительного значения."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = round(new_price, 2)

    def __str__(self) -> str:
        """Строковое представление товара."""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение двух товаров одного класса: сумма произведений цены на количество."""
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного класса")
        return self.__price * self.quantity + other.__price * other.quantity

    def __repr__(self) -> str:
        return (
            f"Product(name={self.name!r}, description={self.description!r}, "
            f"price={self.__price}, quantity={self.quantity})"
        )


class Smartphone(Product):
    """Класс-наследник Product для смартфонов."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self) -> str:
        return (
            f"Smartphone(name={self.name!r}, description={self.description!r}, "
            f"price={self.price}, quantity={self.quantity}, "
            f"efficiency={self.efficiency!r}, model={self.model!r}, "
            f"memory={self.memory}, color={self.color!r})"
        )


class LawnGrass(Product):
    """Класс-наследник Product для травы газонной."""

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
            f"country={self.country!r}, germination_period={self.germination_period!r}, "
            f"color={self.color!r})"
        )


class Category:
    """Класс для описания категории товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[Product] | None = None,
    ):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список товаров категории.
        Принимает только объекты класса Product или его наследников."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий список товаров в виде отформатированной строки."""
        result = ""
        for product in self.__products:
            result += f"{product}\n"
        return result

    def __str__(self) -> str:
        """Строковое представление категории с общим количеством товаров на складе."""
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __repr__(self) -> str:
        return (
            f"Category(name={self.name!r}, description={self.description!r}, "
            f"products={self.__products!r})"
        )


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
    s1 = Smartphone("iPhone 15", "Apple smartphone", 99999.99, 10,
                    "A16 Bionic", "iPhone 15", 128, "чёрный")
    s2 = Smartphone("Samsung Galaxy", "Android smartphone", 79999.99, 5,
                    "Snapdragon 8", "Galaxy S24", 256, "белый")
    print(s1)
    print(f"Сумма смартфонов: {s1 + s2}")

    g1 = LawnGrass("Газонная трава №1", "Для дачи", 500.0, 20,
                   "Россия", "7 дней", "зелёный")
    g2 = LawnGrass("Газонная трава №2", "Для стадиона", 700.0, 15,
                   "Нидерланды", "5 дней", "тёмно-зелёный")
    print(g1)
    print(f"Сумма трав: {g1 + g2}")

    try:
        print(s1 + g1)
    except TypeError as e:
        print(f"Ошибка: {e}")

    c = Category("Электроника", "Смартфоны и гаджеты", [s1, s2])
    print(c)
    print(c.products)

    try:
        c.add_product("не товар")
    except TypeError as e:
        print(f"Ошибка: {e}")
