from src.utils.db_connection import get_connection
from src.utils.hashing import hash_values
import hashlib
import random
from faker import Faker

from ..generators.generate_payments import Payment

faker = Faker()

def insert_address(address):
    row_hash = hash_values(address["street"],address["postal_code"],address["city"],address["country"])
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
    row_hash = hash_values(user["first_name"],user["last_name"],user["email"])
    address_data = {
        "street": user["street"],
        "postal_code": user["postal_code"],
        "city": user["city"],
        "country": user["country"],
        "country_code": user["country_code"]
    }

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
    row_hash = hash_values(product["name"],product["price"],product["category"],product["sku"])
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
            row_hash = hash_values(order["order_status"],random_user_id,shipping_address_id,random_address_id,total_price)
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
                row_hash_order_item = hash_values(order_id, item[1], "1", item[0])
                cur.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, row_hash)
                    VALUES (%s,%s,%s,%s,%s)""",
                    (
                        order_id,
                        item[1],
                        "1",
                        item[0],
                        row_hash_order_item
                    )
                )
def insert_payment():
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT o.order_id, o.order_status, o.total_amount
                FROM orders o
                LEFT JOIN payments p ON o.order_id = p.order_id
                WHERE p.order_id IS NULL
                LIMIT 1
                """
            )

            row = cur.fetchone()

            if row is None:
                return None

            order_id, order_status, order_amount = row

            payment = Payment.generate(order_id, order_status, order_amount)
            row_hash = hash_values(payment["order_id"],payment["payment_method"],order_status,order_amount)

            cur.execute(
                """
                INSERT INTO payments (order_id, payment_method, payment_status, amount, row_hash)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    payment["order_id"],
                    payment["payment_method"],
                    payment["payment_status"],
                    payment["amount"],
                    row_hash
                )
            )
            return None





