from faker import Faker
fake = Faker()
class User:
    @classmethod
    def generate(cls):
        first_name = fake.first_name()
        last_name = fake.last_name()
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "address": fake.address(),
            "phone_number": fake.phone_number()
        }

user_data = User.generate()
print(user_data)