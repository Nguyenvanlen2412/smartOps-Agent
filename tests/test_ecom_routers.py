"""Unit tests for Step 2 expanded E-Commerce endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from mock_api.main import app
from mock_api.database import init_db, engine
from mock_api.seed import seed_initial_data
from mock_api.models import OrderTable, TicketTable


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    init_db()
    with Session(engine) as session:
        seed_initial_data(session)
        # Reset order statuses for deterministic tests
        o1029 = session.exec(select(OrderTable).where(OrderTable.order_id == "VN1029")).first()
        if o1029 and o1029.status != "Processing":
            o1029.status = "Processing"
            session.add(o1029)
        o1025 = session.exec(select(OrderTable).where(OrderTable.order_id == "VN1025")).first()
        if o1025 and o1025.status != "Delivered":
            o1025.status = "Delivered"
            session.add(o1025)
        t0885 = session.exec(select(TicketTable).where(TicketTable.ticket_id == "TKT-0885")).first()
        if t0885:
            t0885.status = "Open"
            session.add(t0885)
        session.commit()


def test_create_order():
    with TestClient(app) as client:
        payload = {
            "user_id": "U00421",
            "customer": "Nguyen Van An",
            "items": [
                {"name": "Logitech MX Master 3S", "quantity": 1, "price_vnd": 2190000}
            ],
            "payment": "VNPay QR",
            "delivery_address": "123 Test Street, Hanoi",
            "note": "Deliver during working hours"
        }
        response = client.post("/orders", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "order_id" in data
        assert data["order_id"].startswith("VN")
        assert data["status"] == "Processing"
        assert len(data["items"]) == 1


def test_list_user_orders():
    with TestClient(app) as client:
        response = client.get("/orders/user/U00421")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1


def test_cancel_order():
    with TestClient(app) as client:
        response = client.post("/orders/VN1029/cancel", json={"reason": "Changed my mind"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Cancelled"
        assert data["cancellation_reason"] == "Changed my mind"


def test_update_delivery_address():
    with TestClient(app) as client:
        response = client.patch("/orders/VN1024/address", json={"new_address": "99 New Address St, Hanoi"})
        assert response.status_code == 200
        data = response.json()
        assert data["delivery_address"] == "99 New Address St, Hanoi"


def test_request_order_return():
    with TestClient(app) as client:
        response = client.post("/orders/VN1025/return", json={"reason": "Defective item", "refund_method": "VNPay"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Return Requested"
        assert data["return_reason"] == "Defective item"


def test_search_and_get_products():
    with TestClient(app) as client:
        # Search query
        response = client.get("/products?query=MacBook")
        assert response.status_code == 200
        products = response.json()
        assert len(products) >= 1
        assert "MacBook" in products[0]["name"]

        # Get single product
        response = client.get("/products/PROD-001")
        assert response.status_code == 200
        product = response.json()
        assert product["name"] == "Samsung Galaxy A55 5G"


def test_user_profile_and_summary():
    with TestClient(app) as client:
        response = client.get("/users/U00421")
        assert response.status_code == 200
        assert response.json()["name"] == "Nguyen Van An"

        response = client.get("/users/U00421/summary")
        assert response.status_code == 200
        summary = response.json()
        assert summary["user_id"] == "U00421"
        assert "active_orders_count" in summary


def test_user_tickets_and_patch():
    with TestClient(app) as client:
        response = client.get("/tickets/user/U00421")
        assert response.status_code == 200
        tickets = response.json()
        assert len(tickets) >= 1

        response = client.patch("/tickets/TKT-0885", json={"status": "In Progress", "assigned_to": "Agent Specialist"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "In Progress"
        assert data["assigned_to"] == "Agent Specialist"
