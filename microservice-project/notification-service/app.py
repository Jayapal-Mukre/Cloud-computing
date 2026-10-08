from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI(title="College Notification Service", version="1.0")
DB = "/app/data/notifications.db"

class Notification(BaseModel):
    student_name: str
    message: str

def db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        message TEXT NOT NULL
    )""")
    conn.commit()
    return conn

@app.get("/health")
def health():
    return {"service": "notification-service", "status": "healthy"}

@app.post("/notifications")
def create_notification(data: Notification):
    conn = db()
    cur = conn.execute(
        "INSERT INTO notifications(student_name, message) VALUES (?, ?)",
        (data.student_name, data.message)
    )
    conn.commit()
    result = {"id": cur.lastrowid, **data.model_dump()}
    conn.close()
    return result

@app.get("/notifications")
def list_notifications():
    conn = db()
    rows = conn.execute("SELECT * FROM notifications ORDER BY id DESC").fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result
