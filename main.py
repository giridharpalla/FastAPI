from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Giridhar first FastAPI Project", version="1.0.0")

# Pydantic models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

# In-memory storage
items_db = ["tomato", "potato", "carrot"]
users_db = []

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to FastAPI!", "version": "1.0.0"}

# Items endpoints
@app.get("/items/")
async def get_items():
    """Get all items"""
    return {"items": items_db}

@app.post("/items/")
async def create_item(item: Item):
    """Create a new item"""
    items_db.append(item.dict())
    return {"message": "Item created", "item": item}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """Get a specific item by ID"""
    if item_id < len(items_db):
        return {"item": items_db[item_id]}
    return {"error": "Item not found"}

# Users endpoints
@app.get("/users/")
async def get_users():
    """Get all users"""
    return {"users": users_db}

@app.post("/users/")
async def create_user(user: User):
    """Create a new user"""
    users_db.append(user.dict())
    return {"message": "User created", "user": user}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id < len(users_db):
        return {"user": users_db[user_id]}
    return {"error": "User not found"}

# Health check
@app.get("/health/")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
