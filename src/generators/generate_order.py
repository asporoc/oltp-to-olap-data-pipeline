import random
import faker
faker = faker.Faker()
STATUSES = {
    "pending", "paid", "shipped", "delivered", "returned", "cancelled"
}

class Order:
    @classmethod
    def generate(cls):
        status = random.choice(list(STATUSES))
        return {
            "order_status": status,
            "numberOfItems": random.randint(1, 5)
        }

def genOrders(number):
    for i in range(number):
        yield Order.generate()



