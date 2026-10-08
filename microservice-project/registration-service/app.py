from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
import requests

app = FastAPI(title="College Registration Service", version="1.0")
DB = "/app/data/registrations.db"
EVENT_URL = os.getenv("EVENT_SERVICE_URL", "http://localhost:8001")
NOTIFICATION_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8003")

class Registration(BaseModel):
    student_name: str
    event_id: int

def db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        event_id INTEGER NOT NULL
    )""")
    conn.commit()
    return conn

@app.get("/health")
def health():
    return {"service": "registration-service", "status": "healthy"}

@app.post("/registrations")
def register(data: Registration):
    try:
        event_response = requests.get(f"{EVENT_URL}/events/{data.event_id}", timeout=3)
    except requests.RequestException:
        raise HTTPException(503, "Event service unavailable")

    if event_response.status_code != 200:
        raise HTTPException(404, "Event not found")

    conn = db()
    duplicate = conn.execute(
        "SELECT id FROM registrations WHERE student_name=? AND event_id=?",
        (data.student_name, data.event_id)
    ).fetchone()
    if duplicate:
        conn.close()
        raise HTTPException(409, "Student already registered")

    cur = conn.execute(
        "INSERT INTO registrations(student_name, event_id) VALUES (?, ?)",
        (data.student_name, data.event_id)
    )
    conn.commit()
    registration = {"id": cur.lastrowid, **data.model_dump()}
    conn.close()

    try:
        requests.post(
            f"{NOTIFICATION_URL}/notifications",
            json={"student_name": data.student_name,
                  "message": f"Registration confirmed for event {data.event_id}"},
            timeout=3
        )
    except requests.RequestException:
        pass

    return registration

@app.get("/registrations")
def list_registrations():
    conn = db()
    rows = conn.execute("SELECT * FROM registrations ORDER BY id").fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result
