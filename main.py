from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="RKLab Backend API")

# In-memory Database (Simple Python List to store items)
items_db = [
    {"id": 1, "name": "Frontend Setup", "status": "Completed"},
    {"id": 2, "name": "Playwright E2E Tests", "status": "Completed"},
]


# Pydantic Model for Request Body validation
class Item(BaseModel):
    name: str
    status: Optional[str] = "Pending"


@app.get("/")
def read_root():
    return {"message": "Welcome to RKLab Backend Server!"}


@app.get("/api/status")
def get_status():
    return {
        "status": "Healthy",
        "lab_name": "RKLab Enterprise Lab",
        "version": "1.0.0",
    }


# 1. GET ALL ITEMS
@app.get("/api/items", response_model=List[dict])
def get_items():
    return items_db


# 2. POST NEW ITEM (Data Creation)
@app.post("/api/items", status_code=201)  # Standard 201 Created
def create_item(item: Item):
    new_id = len(items_db) + 1
    new_item = {"id": new_id, "name": item.name, "status": item.status}
    items_db.append(new_item)
    return {
        "message": "Item created successfully!",
        "data": new_item,
    }