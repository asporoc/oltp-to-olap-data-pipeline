import psycopg2
from src.config import DB_URL

def get_connection():
    return psycopg2.connect(DB_URL)
