import json


class Product:
    """Класс для описания товара в интернет-магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = round(price, 2)
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name} — {self.price} руб. (в наличии: {self.quantity} шт.)"

    def __repr__(self) -> str:
        return (
            f"Product(name={self.name!r}, description={self.description!r}, "
            f"price={self.price}, quantity={self.quantity})"
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
        self.products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.products)

    def __str__(self) -> str:
        return f"{self.name} ({len(self.products)} товаров)"

    def __repr__(self) -> str:
        return (
            f"Category(name={self.name!r}, description={self.description!r}, "
            f"products={self.products!r})"
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
    # Быстрая проверка, что всё работает
    p1 = Product("Laptop", "Good laptop", 999.99, 10)
    p2 = Product("Mouse", "Wireless mouse", 29.90, 50)
    c = Category("Electronics", "All electronics", [p1, p2])
    print(c)
    print(p1)
    print(p2)
    print(f"Категорий: {Category.category_count}, Товаров: {Category.product_count}")
