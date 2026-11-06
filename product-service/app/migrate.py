from app.db import get_conn

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL
)
"""

SEED = [
    ("Laptop", 55000.00, 10),
    ("Headphones", 2500.00, 50),
    ("Keyboard", 1500.00, 30),
]


def main():
    with get_conn() as conn:
        conn.execute(SCHEMA)
        for name, price, stock in SEED:
            conn.execute(
                "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s) "
                "ON CONFLICT (name) DO NOTHING",
                (name, price, stock),
            )
    print("product-service migration complete")


if __name__ == "__main__":
    main()
