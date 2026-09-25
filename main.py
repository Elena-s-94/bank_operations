import json


class Product:
    """Класс для описания товара в интернет-магазине."""

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
        return f"{self.name} — {self.__price} руб. (в наличии: {self.quantity} шт.)"

    def __repr__(self) -> str:
        return (
            f"Product(name={self.name!r}, description={self.description!r}, "
            f"price={self.__price}, quantity={self.quantity})"
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
        """Добавляет продукт в приватный список товаров категории."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий список товаров в виде отформатированной строки."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def __str__(self) -> str:
        return f"{self.name} ({len(self.__products)} товаров)"

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

    p1.price = -10
    p1.price = 1200.00
    print(f"Новая цена laptop: {p1.price}")
