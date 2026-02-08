import random
from faker import Faker

fake = Faker()

CATEGORIES = {
    "Electronics": ["Phone", "Laptop", "Headphones", "Camera"],
    "Books": ["Novel", "Biography", "Cookbook", "Guide"],
    "Clothing": ["T-Shirt", "Jacket", "Jeans", "Sweater"],
    "Home": ["Lamp", "Chair", "Table", "Mug"],
}

class Product:
    @classmethod
    def generate(cls):
        category = random.choice(list(CATEGORIES.keys()))
        item = random.choice(CATEGORIES[category])

        name = f"{fake.word().capitalize()} {item}"

        return {
            "name": name,
            "category": category,
            "price": float(fake.pydecimal(left_digits=3, right_digits=2, positive=True)),
            "sku": fake.unique.ean13(),
            "in_stock": fake.boolean(chance_of_getting_true=80),
        }
def genProducts(number):
    for i in range(number):
        yield Product.generate()
