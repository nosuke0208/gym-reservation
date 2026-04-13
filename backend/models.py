# backend/models.py
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Literal


class ReservationCreate(BaseModel):
    machine: Literal["bench_press", "squat_rack", "deadlift"]
    date: date
    hour: float = Field(ge=10, le=21.5)
    username: str = Field(min_length=1, max_length=20)

    @field_validator("hour")
    @classmethod
    def hour_must_be_half_hour(cls, v: float) -> float:
        if v * 2 % 1 != 0:
            raise ValueError("hour must be a multiple of 0.5")
        return v


class ReservationResponse(BaseModel):
    id: str
    machine: str
    date: date
    hour: float
    username: str
