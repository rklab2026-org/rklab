import hashlib
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

from database import Base, engine, SessionLocal, get_db

# --- Password Hashing Helper (Built-in Security) ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# --- SQLAlchemy Database Table Models ---
class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="Active")

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# Create database tables AFTER table model definition
Base.metadata.create_all(bind=engine)

# Seed initial default data if DB is empty
def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(ItemDB).count() == 0:
            db.add_all([
                ItemDB(name="Sample Item 1", status="Active"),
                ItemDB(name="Sample Item 2", status="Active")
            ])
            db.commit()
    finally:
        db.close()

seed_initial_data()

# --- Pydantic Schemas for API Input/Output Validation ---
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    status: Optional[str] = "Active"

    class Config:
        from_attributes = True

class UserAuth(BaseModel):
    username: str
    password: str

app = FastAPI(title="RKLab Backend API", version="1.0.0")

# Enable CORS so Frontend Website can talk to Backend Server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to RKLab Backend Server!"}

@app.get("/api/status")
def get_status():
    return {
        "status": "Healthy",
        "lab_name": "RKLab Enterprise Lab",
        "version": "1.0.0"
    }

@app.get("/api/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(ItemDB).all()
    return items

@app.post("/api/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item, db: Session = Depends(get_db)):
    if not item.name or item.name.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Item name cannot be empty"
        )
    db_item = ItemDB(name=item.name, status=item.status or "Active")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {
        "message": "Item created successfully!",
        "data": {
            "id": db_item.id,
            "name": db_item.name,
            "status": db_item.status
        }
    }

# ================= USER AUTHENTICATION APIS =================

# 1. SIGN UP (Create New User)
@app.post("/api/signup", status_code=status.HTTP_201_CREATED)
def signup(auth: UserAuth, db: Session = Depends(get_db)):
    # Business Logic 1: Check Empty Input
    if not auth.username.strip() or not auth.password.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username and Password cannot be empty!"
        )

    # Business Logic 2: Check if User Already Exists
    existing_user = db.query(UserDB).filter(UserDB.username == auth.username.strip()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{auth.username}' is already taken! Please choose another."
        )

    # Business Logic 3: Hash Password & Save to DB
    new_user = UserDB(
        username=auth.username.strip(),
        hashed_password=hash_password(auth.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully!",
        "username": new_user.username
    }

# 2. LOGIN (Authenticate User)
@app.post("/api/login")
def login(auth: UserAuth, db: Session = Depends(get_db)):
    # Business Logic 1: Check Empty Input
    if not auth.username.strip() or not auth.password.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username and Password cannot be empty!"
        )

    # Business Logic 2: Find User in DB
    user = db.query(UserDB).filter(UserDB.username == auth.username.strip()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password!"
        )

    # Business Logic 3: Verify Hashed Password
    if user.hashed_password != hash_password(auth.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password!"
        )

    return {
        "message": "Login successful!",
        "username": user.username
    }