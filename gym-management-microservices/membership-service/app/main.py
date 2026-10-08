from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .models import Membership

app = FastAPI(title="Gym Membership Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "service": "Membership Service",
        "status": "running"
    }


@app.post("/memberships")
def create_membership(
    member_id: int,
    plan: str,
    start_date: str,
    end_date: str
):
    db = SessionLocal()

    # Check whether membership already exists
    existing = db.query(Membership).filter(
        Membership.member_id == member_id
    ).first()

    if existing:
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Membership already exists for this member"
        )

    membership = Membership(
        member_id=member_id,
        plan=plan,
        start_date=start_date,
        end_date=end_date,
        status="ACTIVE"
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)
    db.close()

    return {
        "message": "Membership created successfully",
        "membership_id": membership.id,
        "member_id": membership.member_id,
        "status": membership.status
    }


@app.get("/memberships/{member_id}")
def get_membership(member_id: int):

    db = SessionLocal()

    membership = db.query(Membership).filter(
        Membership.member_id == member_id
    ).first()

    db.close()

    if not membership:
        raise HTTPException(
            status_code=404,
            detail="Membership not found"
        )

    return {
        "membership_id": membership.id,
        "member_id": membership.member_id,
        "plan": membership.plan,
        "start_date": membership.start_date,
        "end_date": membership.end_date,
        "status": membership.status
    }


@app.get("/memberships")
def get_all_memberships():

    db = SessionLocal()

    memberships = db.query(Membership).all()

    result = []

    for membership in memberships:
        result.append({
            "membership_id": membership.id,
            "member_id": membership.member_id,
            "plan": membership.plan,
            "start_date": membership.start_date,
            "end_date": membership.end_date,
            "status": membership.status
        })

    db.close()

    return result


@app.put("/memberships/{member_id}")
def update_membership(
    member_id: int,
    plan: str,
    start_date: str,
    end_date: str,
    status: str
):

    db = SessionLocal()

    membership = db.query(Membership).filter(
        Membership.member_id == member_id
    ).first()

    if not membership:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Membership not found"
        )

    membership.plan = plan
    membership.start_date = start_date
    membership.end_date = end_date
    membership.status = status

    db.commit()
    db.close()

    return {
        "message": "Membership updated successfully"
    }


@app.delete("/memberships/{member_id}")
def delete_membership(member_id: int):
    db = SessionLocal()

    membership = db.query(Membership).filter(
        Membership.member_id == member_id
    ).first()

    if not membership:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Membership not found"
        )

    db.delete(membership)
    db.commit()
    db.close()

    return {
        "message": "Membership deleted successfully"
    }