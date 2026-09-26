"""
database.py
SQLite persistence for FitBuddy, via SQLAlchemy ORM.

Tables:
    users  -> one row per registered user
    plans  -> one row per user's plan (original + updated + nutrition tip)

Functions (used by routes.py):
    save_user(user: UserInput)
    save_plan(user_id, original_plan, nutrition_tip)
    update_plan(user_id, updated_plan)
    get_original_plan(user_id) -> str | None
    get_user(user_id) -> User | None
    get_all_users() -> list[User]
    get_all_plans() -> list[Plan]
    delete_user(user_id)
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "fitbuddy.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)

    plan = relationship("Plan", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), unique=True, nullable=False)
    original_plan = Column(Text, nullable=True)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)

    user = relationship("User", back_populates="plan")


def init_db():
    """Create tables if they don't already exist. Called once on startup."""
    Base.metadata.create_all(bind=engine)


def _session():
    return SessionLocal()


# ---------- Users ----------

def save_user(user_input) -> None:
    """Insert a new user, or update their profile fields if user_id already exists."""
    db = _session()
    try:
        existing = db.query(User).filter(User.user_id == user_input.user_id).first()
        if existing:
            existing.username = user_input.username
            existing.age = user_input.age
            existing.weight = user_input.weight
            existing.goal = user_input.goal
            existing.intensity = user_input.intensity
        else:
            db.add(User(
                user_id=user_input.user_id,
                username=user_input.username,
                age=user_input.age,
                weight=user_input.weight,
                goal=user_input.goal,
                intensity=user_input.intensity,
            ))
        db.commit()
    finally:
        db.close()


def get_user(user_id: str):
    db = _session()
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    finally:
        db.close()


def get_all_users():
    db = _session()
    try:
        return db.query(User).all()
    finally:
        db.close()


def delete_user(user_id: str) -> None:
    db = _session()
    try:
        db.query(Plan).filter(Plan.user_id == user_id).delete()
        db.query(User).filter(User.user_id == user_id).delete()
        db.commit()
    finally:
        db.close()


# ---------- Plans ----------

def save_plan(user_id: str, original_plan: str, nutrition_tip: str) -> None:
    """Create or overwrite the ORIGINAL plan + nutrition tip for a user."""
    db = _session()
    try:
        existing = db.query(Plan).filter(Plan.user_id == user_id).first()
        if existing:
            existing.original_plan = original_plan
            existing.nutrition_tip = nutrition_tip
            existing.updated_plan = None  # a fresh generation resets any prior revision
        else:
            db.add(Plan(user_id=user_id, original_plan=original_plan, nutrition_tip=nutrition_tip))
        db.commit()
    finally:
        db.close()


def update_plan(user_id: str, updated_plan: str) -> None:
    """Store the feedback-revised plan, keeping the original plan intact."""
    db = _session()
    try:
        plan = db.query(Plan).filter(Plan.user_id == user_id).first()
        if plan:
            plan.updated_plan = updated_plan
            db.commit()
    finally:
        db.close()


def get_original_plan(user_id: str):
    db = _session()
    try:
        plan = db.query(Plan).filter(Plan.user_id == user_id).first()
        return plan.original_plan if plan else None
    finally:
        db.close()


def get_all_plans():
    db = _session()
    try:
        return db.query(Plan).all()
    finally:
        db.close()
