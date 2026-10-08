from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .models import Member

app = FastAPI(title="Gym Member Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "service": "Member Service",
        "status": "running"
    }


@app.post("/members")
def create_member(
    name: str,
    age: int,
    phone: str,
    email: str
):
    db = SessionLocal()

    member = Member(
        name=name,
        age=age,
        phone=phone,
        email=email
    )

    db.add(member)
    db.commit()
    db.refresh(member)
    db.close()

    return {
        "message": "Member created successfully",
        "member_id": member.id
    }


@app.get("/members")
def get_members():

    db = SessionLocal()

    members = db.query(Member).all()

    result = []

    for member in members:
        result.append({
            "id": member.id,
            "name": member.name,
            "age": member.age,
            "phone": member.phone,
            "email": member.email
        })

    db.close()

    return result


@app.get("/members/{member_id}")
def get_member(member_id: int):

    db = SessionLocal()

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    db.close()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return {
        "id": member.id,
        "name": member.name,
        "age": member.age,
        "phone": member.phone,
        "email": member.email
    }


@app.put("/members/{member_id}")
def update_member(
    member_id: int,
    name: str,
    age: int,
    phone: str,
    email: str
):

    db = SessionLocal()

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    member.name = name
    member.age = age
    member.phone = phone
    member.email = email

    db.commit()
    db.close()

    return {
        "message": "Member updated successfully"
    }


@app.delete("/members/{member_id}")
def delete_member(member_id: int):

    db = SessionLocal()

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    db.delete(member)
    db.commit()
    db.close()

    return {
        "message": "Member deleted successfully"
    }