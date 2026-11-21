import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Environment variables load cheyadam
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./rklab.db"

# SQLite multithreading support optimization
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# FastAPI Request Dependency for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()