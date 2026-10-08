import requests
import sys

BASE = {
    "event": "http://localhost:8001",
    "registration": "http://localhost:8002",
    "notification": "http://localhost:8003",
}

passed = 0
failed = 0
event_id = None

def check(name, fn):
    global passed, failed
    try:
        fn()
        print(f"[PASS] {name}")
        passed += 1
    except Exception as exc:
        print(f"[FAIL] {name}: {exc}")
        failed += 1

def event_health():
    assert requests.get(BASE["event"] + "/health", timeout=3).status_code == 200

def registration_health():
    assert requests.get(BASE["registration"] + "/health", timeout=3).status_code == 200

def notification_health():
    assert requests.get(BASE["notification"] + "/health", timeout=3).status_code == 200

def create_event():
    global event_id
    r = requests.post(
        BASE["event"] + "/events",
        json={"name":"Cloud Computing Seminar","venue":"Lab 1","capacity":100},
        timeout=3
    )
    assert r.status_code == 200
    event_id = r.json()["id"]

def register_student():
    r = requests.post(
        BASE["registration"] + "/registrations",
        json={"student_name":"Test Student","event_id":event_id},
        timeout=3
    )
    assert r.status_code == 200

def notifications_created():
    r = requests.get(BASE["notification"] + "/notifications", timeout=3)
    assert r.status_code == 200
    assert any(n["student_name"] == "Test Student" for n in r.json())

check("Event service health", event_health)
check("Registration service health", registration_health)
check("Notification service health", notification_health)
check("Create event", create_event)
check("Register student", register_student)
check("Notification created", notifications_created)

print(f"\nPassed: {passed}  Failed: {failed}")
sys.exit(1 if failed else 0)
