from .db_connection import get_connection
import hashlib
def hash_address(address):
    raw = f"{address['street']}{address['postal_code']}{address['city']}{address['country']}"
    return hashlib.sha256(raw.encode()).hexdigest()
def hash_user(user):
    raw = f"{user['first_name']}{user['last_name']}{user['email']}"
    return hashlib.sha256(raw.encode()).hexdigest()
def hash_product(product):
    raw = f"{product['name']}{product['price']}{product['category']}{product['sku']}"
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
