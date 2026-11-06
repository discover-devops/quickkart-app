from app.db import get_conn

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
"""

SEED = [
    ("Asha", "asha@quickkart.example"),
    ("Ravi", "ravi@quickkart.example"),
    ("Meera", "meera@quickkart.example"),
]


def main():
    with get_conn() as conn:
        conn.execute(SCHEMA)
        for name, email in SEED:
            conn.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) "
                "ON CONFLICT (email) DO NOTHING",
                (name, email),
            )
    print("user-service migration complete")


if __name__ == "__main__":
    main()
