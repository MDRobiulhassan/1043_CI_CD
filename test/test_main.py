from fastapi.testclient import TestClient
from src.main import api, tickets

client = TestClient(api)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Message": "Welcome to the Ticket Booking System"}


def test_add_ticket():
    tickets.clear()
    new_ticket = {
        "id": 1,
        "flight_name": "AirX",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    response = client.post("/ticket", json=new_ticket)
    assert response.status_code == 200
    assert response.json() == new_ticket
    assert len(tickets) == 1


def test_get_tickets():
    response = client.get("/ticket")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["id"] == 1


def test_update_ticket():
    updated_ticket = {
        "id": 1,
        "flight_name": "AirY",
        "flight_date": "2025-10-20",
        "flight_time": "16:00",
        "destination": "London"
    }
    response = client.put("/ticket/1", json=updated_ticket)
    assert response.status_code == 200
    assert response.json() == updated_ticket
    assert tickets[0].flight_name == "AirY"


def test_update_ticket_not_found():
    updated_ticket = {
        "id": 2,
        "flight_name": "AirZ",
        "flight_date": "2025-11-01",
        "flight_time": "18:00",
        "destination": "Tokyo"
    }
    response = client.put("/ticket/999", json=updated_ticket)
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket Not Found"}


def test_delete_ticket():
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert len(tickets) == 0


def test_delete_ticket_not_found():
    response = client.delete("/ticket/12345")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}
