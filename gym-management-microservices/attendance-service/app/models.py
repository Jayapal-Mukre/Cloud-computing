from sqlalchemy import Column, Integer, String
from .database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, index=True)
    check_in = Column(String)
    check_out = Column(String, nullable=True)
    status = Column(String)