import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.db import get_conn

SERVICE_NAME = "order-service"
APP_VERSION = os.getenv("APP_VERSION", "local")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8002")

app = FastAPI(title="QuickKart Order Service")


class OrderRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(gt=0)


def version_info():
    return {"service": SERVICE_NAME, "version": APP_VERSION, "environment": ENVIRONMENT}


def fetch(url, not_found_message):
    try:
        response = httpx.get(url, timeout=3)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"dependency not reachable: {exc}")
    if response.status_code == 404:
        raise HTTPException(status_code=400, detail=not_found_message)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"dependency error: {url}")
    return response.json()


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


@app.get("/api/orders/version")
def public_version():
    return version_info()


@app.get("/api/orders")
def list_orders():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, user_id, product_id, quantity, total, created_at "
            "FROM orders ORDER BY id"
        ).fetchall()
    return [
        {
            "id": r[0],
            "user_id": r[1],
            "product_id": r[2],
            "quantity": r[3],
            "total": float(r[4]),
            "created_at": r[5].isoformat(),
        }
        for r in rows
    ]


@app.post("/api/orders", status_code=201)
def create_order(order: OrderRequest):
    user = fetch(f"{USER_SERVICE_URL}/api/users/{order.user_id}", "user not found")
    product = fetch(
        f"{PRODUCT_SERVICE_URL}/api/products/{order.product_id}", "product not found"
    )
    total = product["price"] * order.quantity
    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO orders (user_id, product_id, quantity, total) "
            "VALUES (%s, %s, %s, %s) RETURNING id",
            (order.user_id, order.product_id, order.quantity, total),
        ).fetchone()
    return {
        "order_id": row[0],
        "user": user["name"],
        "product": product["name"],
        "quantity": order.quantity,
        "total": total,
    }
