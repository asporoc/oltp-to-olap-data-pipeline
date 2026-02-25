from faker import Faker
import random


FAKERS = {
    "DE": Faker("de_DE"),  # Germany
    "FR": Faker("fr_FR"),  # France
    "IT": Faker("it_IT"),  # Italy
    "SE": Faker("sv_SE"),  # Sweden
    "GB": Faker("en_GB"),  # United Kingdom
}
class User:
    @classmethod
    def generate(cls):
        country_code = random.choice(list(FAKERS.keys()))
        fake = FAKERS[country_code]

        first_name = fake.first_name()
        last_name = fake.last_name()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@example.{country_code.lower()}",
            "street": fake.street_address(),
            "postal_code": fake.postcode(),
            "city": fake.city(),
            "country": fake.current_country(),
            "country_code": country_code,
            "phone_number": fake.phone_number(),
        }
def genUsers(number):
    for i in range(number):
        yield User.generate()

#for users in genUsers(10):
#    print(users)

