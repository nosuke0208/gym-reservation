# backend/tests/test_api.py
from datetime import date
from pydantic import ValidationError
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from models import ReservationCreate


def test_reservation_create_valid():
    r = ReservationCreate(
        machine="bench_press",
        date=date(2026, 4, 8),
        hour=10,
        username="田中"
    )
    assert r.machine == "bench_press"
    assert r.hour == 10


def test_reservation_create_invalid_machine():
    with pytest.raises(ValidationError):
        ReservationCreate(machine="invalid", date=date(2026, 4, 8), hour=10, username="田中")


def test_reservation_create_invalid_hour():
    with pytest.raises(ValidationError):
        ReservationCreate(machine="bench_press", date=date(2026, 4, 8), hour=9, username="田中")


def test_reservation_create_username_too_long():
    with pytest.raises(ValidationError):
        ReservationCreate(
            machine="bench_press",
            date=date(2026, 4, 8),
            hour=10,
            username="a" * 21
        )


def test_get_reservations_returns_list(api_client):
    client, mock_sb = api_client
    mock_sb.table.return_value.select.return_value \
        .eq.return_value.gte.return_value.lte.return_value \
        .execute.return_value.data = [
            {"id": "uuid-1", "machine": "bench_press",
             "date": "2026-04-08", "hour": 10, "username": "田中"}
        ]

    resp = client.get("/reservations?machine=bench_press&start=2026-04-07&end=2026-04-13")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["username"] == "田中"


from postgrest.exceptions import APIError


def test_post_reservation_success(api_client):
    client, mock_sb = api_client
    mock_sb.table.return_value.insert.return_value.execute.return_value.data = [
        {"id": "uuid-2", "machine": "bench_press",
         "date": "2026-04-08", "hour": 14, "username": "佐藤"}
    ]

    resp = client.post("/reservations", json={
        "machine": "bench_press",
        "date": "2026-04-08",
        "hour": 14,
        "username": "佐藤"
    })
    assert resp.status_code == 201
    assert resp.json()["username"] == "佐藤"


def test_post_reservation_conflict(api_client):
    client, mock_sb = api_client
    api_error = APIError({"code": "23505", "message": "duplicate key"})
    mock_sb.table.return_value.insert.return_value.execute.side_effect = api_error

    resp = client.post("/reservations", json={
        "machine": "bench_press",
        "date": "2026-04-08",
        "hour": 14,
        "username": "鈴木"
    })
    assert resp.status_code == 409
    assert "予約されています" in resp.json()["detail"]


def test_delete_reservation_success(api_client):
    client, mock_sb = api_client
    mock_sb.table.return_value.select.return_value \
        .eq.return_value.limit.return_value.execute.return_value.data = [
            {"id": "uuid-3", "machine": "bench_press",
             "date": "2026-04-08", "hour": 10, "username": "田中"}
        ]
    mock_sb.table.return_value.delete.return_value \
        .eq.return_value.execute.return_value.data = []

    resp = client.delete("/reservations/uuid-3?username=田中")
    assert resp.status_code == 200


def test_delete_reservation_wrong_username(api_client):
    client, mock_sb = api_client
    mock_sb.table.return_value.select.return_value \
        .eq.return_value.limit.return_value.execute.return_value.data = [
            {"id": "uuid-3", "machine": "bench_press",
             "date": "2026-04-08", "hour": 10, "username": "田中"}
        ]

    resp = client.delete("/reservations/uuid-3?username=別人")
    assert resp.status_code == 403


def test_delete_reservation_not_found(api_client):
    client, mock_sb = api_client
    mock_sb.table.return_value.select.return_value \
        .eq.return_value.limit.return_value.execute.return_value.data = []

    resp = client.delete("/reservations/nonexistent?username=田中")
    assert resp.status_code == 404
