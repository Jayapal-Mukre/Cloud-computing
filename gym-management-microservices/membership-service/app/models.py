from sqlalchemy import Column, Integer, String
from .database import Base


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, unique=True, index=True)
    plan = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    status = Column(String)