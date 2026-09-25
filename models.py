from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    goal = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
