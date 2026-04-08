# backend/main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date as date_type
from database import supabase
from models import ReservationCreate, ReservationResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # デプロイ後にVercelのURLに絞る
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


@app.get("/reservations", response_model=list[ReservationResponse])
def get_reservations(
    machine: str = Query(...),
    start: date_type = Query(...),
    end: date_type = Query(...),
):
    result = (
        supabase.table("reservations")
        .select("*")
        .eq("machine", machine)
        .gte("date", str(start))
        .lte("date", str(end))
        .execute()
    )
    return result.data
