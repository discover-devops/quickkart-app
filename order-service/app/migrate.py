from app.db import get_conn

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
"""


def main():
    with get_conn() as conn:
        conn.execute(SCHEMA)
    print("order-service migration complete")


if __name__ == "__main__":
    main()
