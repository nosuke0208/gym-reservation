# backend/main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date as date_type
from database import supabase
from models import ReservationCreate, ReservationResponse
from postgrest.exceptions import APIError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # デプロイ後にVercelのURLに絞る
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


@app.post("/reservations", response_model=ReservationResponse, status_code=201)
def create_reservation(body: ReservationCreate):
    try:
        result = (
            supabase.table("reservations")
            .insert({
                "machine": body.machine,
                "date": str(body.date),
                "hour": body.hour,
                "username": body.username,
            })
            .execute()
        )
        return result.data[0]
    except APIError as e:
        if e.code == "23505":
            raise HTTPException(status_code=409, detail="この枠はすでに予約されています")
        raise HTTPException(status_code=500, detail="サーバーエラー")


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
