import os
from datetime import datetime
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .models import Attendance

app = FastAPI(title="Gym Attendance Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Microservice URLs
# --------------------------------------------------

MEMBER_SERVICE_URL = os.getenv("MEMBER_SERVICE_URL", "http://member-service:8000")
MEMBERSHIP_SERVICE_URL = os.getenv("MEMBERSHIP_SERVICE_URL", "http://membership-service:8000")



# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "service": "Attendance Service",
        "status": "running"
    }


# --------------------------------------------------
# Check-In
# --------------------------------------------------

@app.post("/attendance/checkin")
async def checkin(member_id: int):

    # ----------------------------------------------
    # 1. Check Member Service
    # ----------------------------------------------

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:

            member_response = await client.get(
                f"{MEMBER_SERVICE_URL}/members/{member_id}"
            )

            if member_response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail="Member not found"
                )

            if member_response.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail="Member Service unavailable"
                )

            member = member_response.json()

            # ------------------------------------------
            # 2. Check Membership Service
            # ------------------------------------------

            membership_response = await client.get(
                f"{MEMBERSHIP_SERVICE_URL}/memberships/{member_id}"
            )

            if membership_response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail="Membership not found"
                )

            if membership_response.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail="Membership Service unavailable"
                )

            membership = membership_response.json()

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to communicate with another service: {str(e)}"
        )

    # ----------------------------------------------
    # 3. Check Membership Status
    # ----------------------------------------------

    membership_status = str(
        membership.get("status", "")
    ).strip().upper()

    if membership_status != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail=f"Membership is not active. Current status: {membership_status}"
        )

    # ----------------------------------------------
    # 4. Save Attendance
    # ----------------------------------------------

    db = SessionLocal()

    try:

        attendance = Attendance(
            member_id=member_id,
            check_in=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            check_out=None,
            status="PRESENT"
        )

        db.add(attendance)
        db.commit()
        db.refresh(attendance)

        return {
            "message": "Check-in successful",
            "attendance_id": attendance.id,
            "member_id": member_id,
            "member_name": member.get("name"),
            "membership_plan": membership.get("plan"),
            "membership_status": membership_status,
            "status": "PRESENT",
            "check_in": attendance.check_in
        }

    finally:
        db.close()


# --------------------------------------------------
# Check-Out
# --------------------------------------------------

@app.post("/attendance/checkout/{attendance_id}")
def checkout(attendance_id: int):

    db = SessionLocal()

    try:

        attendance = db.query(Attendance).filter(
            Attendance.id == attendance_id
        ).first()

        if not attendance:
            raise HTTPException(
                status_code=404,
                detail="Attendance record not found"
            )

        if attendance.check_out is not None:
            raise HTTPException(
                status_code=400,
                detail="Member already checked out"
            )

        attendance.check_out = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        attendance.status = "COMPLETED"

        db.commit()
        db.refresh(attendance)

        return {
            "message": "Check-out successful",
            "attendance_id": attendance.id,
            "member_id": attendance.member_id,
            "check_out": attendance.check_out,
            "status": attendance.status
        }

    finally:
        db.close()


# --------------------------------------------------
# Get Attendance History
# --------------------------------------------------

@app.get("/attendance/{member_id}")
def get_attendance(member_id: int):

    db = SessionLocal()

    try:

        records = db.query(Attendance).filter(
            Attendance.member_id == member_id
        ).all()

        result = []

        for record in records:

            result.append({
                "attendance_id": record.id,
                "member_id": record.member_id,
                "check_in": record.check_in,
                "check_out": record.check_out,
                "status": record.status
            })

        return result

    finally:
        db.close()


# --------------------------------------------------
# Get All Attendance Records (Global Activity Feed)
# --------------------------------------------------

@app.get("/attendance")
def get_all_attendance():
    db = SessionLocal()
    try:
        records = db.query(Attendance).order_by(Attendance.id.desc()).all()
        result = []
        for record in records:
            result.append({
                "attendance_id": record.id,
                "member_id": record.member_id,
                "check_in": record.check_in,
                "check_out": record.check_out,
                "status": record.status
            })
        return result
    finally:
        db.close()


# --------------------------------------------------
# Delete Attendance Record
# --------------------------------------------------

@app.delete("/attendance/{attendance_id}")
def delete_attendance(attendance_id: int):
    db = SessionLocal()
    try:
        attendance = db.query(Attendance).filter(
            Attendance.id == attendance_id
        ).first()
        if not attendance:
            raise HTTPException(
                status_code=404,
                detail="Attendance record not found"
            )
        db.delete(attendance)
        db.commit()
        return {"message": "Attendance record deleted successfully"}
    finally:
        db.close()