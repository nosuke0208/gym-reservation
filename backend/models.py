# backend/models.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Literal


class ReservationCreate(BaseModel):
    machine: Literal["bench_press", "squat_rack", "deadlift"]
    date: date
    hour: int = Field(ge=10, le=21)
    username: str = Field(min_length=1, max_length=20)


class ReservationResponse(BaseModel):
    id: str
    machine: str
    date: date
    hour: int
    username: str
