import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from db_models import TicketDB

SQLALCHEMY_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


def sample_ticket():
    return {
        "title": "VPN not working",
        "description": "Unable to connect to company VPN",
        "category": "Network",
        "priority": "High",
    }


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "IT Ticket Management API is running"


def test_create_ticket():
    response = client.post("/tickets", json=sample_ticket())
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket created successfully"
    assert response.json()["ticket"]["title"] == "VPN not working"
    assert "id" in response.json()["ticket"]


def test_list_tickets():
    client.post("/tickets", json=sample_ticket())
    response = client.get("/tickets")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "VPN not working"


def test_get_ticket():
    create_response = client.post("/tickets", json=sample_ticket())
    ticket_id = create_response.json()["ticket"]["id"]

    response = client.get(f"/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ticket_id


def test_get_missing_ticket():
    response = client.get("/tickets/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_update_ticket():
    create_response = client.post("/tickets", json=sample_ticket())
    ticket_id = create_response.json()["ticket"]["id"]

    updated_ticket = sample_ticket()
    updated_ticket["title"] = "VPN fixed"

    response = client.put(f"/tickets/{ticket_id}", json=updated_ticket)
    assert response.status_code == 200
    assert response.json()["ticket"]["title"] == "VPN fixed"


def test_delete_ticket():
    create_response = client.post("/tickets", json=sample_ticket())
    ticket_id = create_response.json()["ticket"]["id"]

    response = client.delete(f"/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["ticket_id"] == ticket_id

    get_response = client.get(f"/tickets/{ticket_id}")
    assert get_response.status_code == 404


def test_delete_missing_ticket():
    response = client.delete("/tickets/9999")
    assert response.status_code == 404
