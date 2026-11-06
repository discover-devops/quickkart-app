import os

import psycopg


def get_conn():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "quickkart"),
        user=os.getenv("DB_USER", "quickkart"),
        password=os.getenv("DB_PASSWORD", "quickkart"),
        connect_timeout=3,
    )
