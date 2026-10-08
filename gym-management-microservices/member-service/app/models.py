from sqlalchemy import Column, Integer, String
from .database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    phone = Column(String)
    email = Column(String)