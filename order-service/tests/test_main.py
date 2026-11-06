from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_version():
    response = client.get("/api/orders/version")
    assert response.status_code == 200
    assert response.json()["service"] == "order-service"


def test_quantity_must_be_positive():
    response = client.post(
        "/api/orders", json={"user_id": 1, "product_id": 1, "quantity": 0}
    )
    assert response.status_code == 422
