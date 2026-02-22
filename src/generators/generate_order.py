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
            "status": status
        }

def genOrders(number):
    for i in range(number):
        yield Order.generate()

for order in genOrders(3):
    print(order)

