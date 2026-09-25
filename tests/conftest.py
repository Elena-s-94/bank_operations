import pytest
from main import Product, Category


@pytest.fixture
def sample_product() -> Product:
    return Product(name="Laptop", description="Good laptop", price=999.99, quantity=10)


@pytest.fixture
def another_product() -> Product:
    return Product(name="Mouse", description="Wireless mouse", price=29.90, quantity=50)


@pytest.fixture
def sample_category(sample_product, another_product) -> Category:
    return Category(
        name="Electronics",
        description="All electronics",
        products=[sample_product, another_product],
    )
