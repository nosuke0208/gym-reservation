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
