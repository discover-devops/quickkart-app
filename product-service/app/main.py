import os

from fastapi import FastAPI, HTTPException

from app.db import get_conn

SERVICE_NAME = "product-service"
APP_VERSION = os.getenv("APP_VERSION", "local")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

app = FastAPI(title="QuickKart Product Service")


def version_info():
    return {"service": SERVICE_NAME, "version": APP_VERSION, "environment": ENVIRONMENT}


@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE_NAME}


@app.get("/ready")
def ready():
    try:
        with get_conn() as conn:
            conn.execute("SELECT 1")
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database not reachable: {exc}")
    return {"status": "ready", "service": SERVICE_NAME}


@app.get("/version")
def version():
    return version_info()


@app.get("/api/products/version")
def public_version():
    return version_info()


@app.get("/api/products")
def list_products():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, name, price, stock FROM products ORDER BY id"
        ).fetchall()
    return [
        {"id": r[0], "name": r[1], "price": float(r[2]), "stock": r[3]} for r in rows
    ]


@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, name, price, stock FROM products WHERE id = %s",
            (product_id,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="product not found")
    return {"id": row[0], "name": row[1], "price": float(row[2]), "stock": row[3]}
