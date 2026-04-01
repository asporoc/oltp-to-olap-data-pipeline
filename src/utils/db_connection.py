import psycopg2


def get_connection(url):
    return psycopg2.connect(url)
