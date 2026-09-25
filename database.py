import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Render la DATABASE_URL irukkum, illana local sqlite
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./fitbuddy.db"

# sqlite ku check_same_thread venda
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    # models import panni table create pannurom
    try:
        from models import Base as ModelsBase
        # models.py la irukkura Base ah use pannurom
        import models
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        # fallback - namma Base ah create pannurom
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e2:
            print(f"DB init error: {e2}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
