from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

from database import Base, engine, SessionLocal, get_db

# --- SQLAlchemy Database Table Model ---
class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_primary_key=True, index=True) if False else Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="Active")

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

# --- Pydantic Schema for API Input/Output Validation ---
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    status: Optional[str] = "Active"

    class Config:
        from_attributes = True

app = FastAPI(title="RKLab Backend API", version="1.0.0")

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