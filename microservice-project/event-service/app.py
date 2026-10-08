from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI(title="College Event Service", version="1.0")
DB = "/app/data/events.db"

class Event(BaseModel):
    name: str
    venue: str
    capacity: int

def db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        venue TEXT NOT NULL,
        capacity INTEGER NOT NULL
    )""")
    conn.commit()
    return conn

@app.get("/health")
def health():
    return {"service": "event-service", "status": "healthy"}

@app.post("/events")
def create_event(event: Event):
    if event.capacity <= 0:
        raise HTTPException(400, "Capacity must be positive")
    conn = db()
    cur = conn.execute(
        "INSERT INTO events(name, venue, capacity) VALUES (?, ?, ?)",
        (event.name, event.venue, event.capacity)
    )
    conn.commit()
    result = {"id": cur.lastrowid, **event.model_dump()}
    conn.close()
    return result

@app.get("/events")
def list_events():
    conn = db()
    rows = conn.execute("SELECT * FROM events ORDER BY id").fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result

@app.get("/events/{event_id}")
def get_event(event_id: int):
    conn = db()
    row = conn.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Event not found")
    return dict(row)
