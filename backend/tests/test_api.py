from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_products():
    r = client.get("/api/products")
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_product_not_found():
    assert client.get("/api/products/999").status_code == 404


def test_contact_valid():
    r = client.post("/api/contact", json={
        "name": "Ada", "email": "ada@example.com",
        "subject": "Hello", "message": "Test"})
    assert r.status_code == 201


def test_contact_invalid_email():
    r = client.post("/api/contact", json={
        "name": "Ada", "email": "not-an-email",
        "subject": "Hello", "message": "Test"})
    assert r.status_code == 422