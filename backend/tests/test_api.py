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
