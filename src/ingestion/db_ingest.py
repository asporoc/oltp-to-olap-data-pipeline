from .db_connection import get_connection
import hashlib
import random
from faker import Faker

faker = Faker()

from ..generators.generate_order import genOrders


def hash_address(address):
    raw = f"{address['street']}{address['postal_code']}{address['city']}{address['country']}"
    return hashlib.sha256(raw.encode()).hexdigest()
def hash_user(user):
    raw = f"{user['first_name']}{user['last_name']}{user['email']}"
    return hashlib.sha256(raw.encode()).hexdigest()
def hash_product(product):
    raw = f"{product['name']}{product['price']}{product['category']}{product['sku']}"
    return hashlib.sha256(raw.encode()).hexdigest()
def hash_order(order, user_id, shipping_address_id, billing_address_id, total):
    raw = f"{order['order_status']}{user_id}{shipping_address_id}{billing_address_id}{total}"
    print(raw)
    return hashlib.sha256(raw.encode()).hexdigest()
def hash_order_item(order_id, product_id, quantity, unit_price):
    raw = f"{order_id}{product_id}{quantity}{unit_price}"
    return hashlib.sha256(raw.encode()).hexdigest()

def insert_address(address):
    row_hash = hash_address(address)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO address (street, postal_code, city, country, row_hash)
                VALUES (%s,%s,%s,%s,%s)
                RETURNING address_id
                """,
                (
                    address["street"],
                    address["postal_code"],
                    address["city"],
                    address["country"],
                    row_hash
                )
            )
            address_id = cur.fetchone()[0]
        conn.commit()
    return address_id

def insert_user(user):
    row_hash = hash_user(user)
    # Extract address data from user dict
    address_data = {
        "street": user["street"],
        "postal_code": user["postal_code"],
        "city": user["city"],
        "country": user["country"],
        "country_code": user["country_code"]
    }

    # Insert address and get id
    address_id = insert_address(address_data)
    print(address_id)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (first_name, last_name, email, phone_number, address_id, row_hash)
                VALUES (%s,%s,%s,%s,%s, %s)
                """,
                (
                    user["first_name"],
                    user["last_name"],
                    user["email"],
                    user["phone_number"],
                    address_id,
                    row_hash
                )
            )
        conn.commit()

def insert_product(product):
    row_hash = hash_product(product)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO products (name, price, category, sku, row_hash)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    product["name"],
                    product["price"],
                    product["category"],
                    product["sku"],
                    row_hash
                )
            )
        conn.commit()

def insert_order(order):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT user_id,address_id FROM users ORDER BY RANDOM() LIMIT 1
                """
            )
            random_ids = cur.fetchone()
            random_user_id = random_ids[0]
            random_address_id = random_ids[1]
            if random.random() < 0.7:
                shipping_address_id = random_address_id
            else:
                new_address = {
                    "street": faker.street_address(),
                    "postal_code": faker.postcode(),
                    "city": faker.city(),
                    "country": faker.country()
                }
                shipping_address_id = insert_address(new_address)

            cur.execute(
                """
                SELECT price, product_id FROM products ORDER BY RANDOM() LIMIT %s
                """,
                (order["numberOfItems"],)
            )
            random_products = cur.fetchall()
            total_price = sum(product[0] for product in random_products)
            row_hash = hash_order(order, random_user_id, shipping_address_id, random_address_id, total_price)
            cur.execute(
                """
                INSERT INTO orders (user_id, shipping_address_id, billing_address_id, order_status, total_amount, row_hash)
                VALUES (%s,%s,%s,%s,%s,%s)
                RETURNING order_id""",
                (
                    random_user_id,
                    shipping_address_id,
                    random_address_id,
                    order["order_status"],
                    total_price,
                    row_hash
                )
            )
            order_id = cur.fetchone()[0]
            for item in random_products:
                row_hash_order_item = (order_id, item[1], '1', item[0])
                cur.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, row_hash)
                    VALUES (%s,%s,%s,%s,%s)""",
                    (
                        order_id,
                        item[1],
                        '1',
                        item[0],
                        row_hash_order_item
                    )
                )




