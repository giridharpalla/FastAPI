from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import Optional
import logging

app = FastAPI(title="Giridhar first FastAPI Project", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom exception class
class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.message = f"Item with ID {item_id} not found"

class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"User with ID {user_id} not found"

# Exception handlers
@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request, exc: ItemNotFoundException):
    logger.warning(f"Item not found: {exc.message}")
    return {
        "error": exc.message,
        "status_code": 404,
        "details": f"Item ID {exc.item_id} does not exist"
    }

@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request, exc: UserNotFoundException):
    logger.warning(f"User not found: {exc.message}")
    return {
        "error": exc.message,
        "status_code": 404,
        "details": f"User ID {exc.user_id} does not exist"
    }

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

@app.get("/items/")
async def get_items():
    """Get all items"""
    try:
        if not items_db:
            logger.info("Retrieving empty items list")
            return {"items": [], "count": 0}
        logger.info(f"Retrieved {len(items_db)} items")
        return {"items": items_db, "count": len(items_db)}
    except Exception as e:
        logger.error(f"Error retrieving items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving items"
        )

@app.post("/items/")
async def create_item(item: Item):
    """Create a new item"""
    try:
        # Validate price
        if item.price < 0:
            logger.warning("Attempted to create item with negative price")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Price cannot be negative"
            )
        
        # Validate name
        if not item.name or len(item.name.strip()) == 0:
            logger.warning("Attempted to create item with empty name")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item name cannot be empty"
            )
        
        item_dict = item.dict()
        items_db.append(item_dict)
        logger.info(f"Item created: {item.name}")
        return {
            "message": "Item created successfully",
            "item": item_dict,
            "total_items": len(items_db)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred while creating item"
        )

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """Get a specific item by ID"""
    try:
        # Validate item_id
        if item_id < 0:
            logger.warning(f"Attempted to get item with negative ID: {item_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item ID cannot be negative"
            )
        
        if item_id >= len(items_db):
            logger.warning(f"Item not found: ID {item_id}")
            raise ItemNotFoundException(item_id)
        
        logger.info(f"Retrieved item ID: {item_id}")
        return {"item": items_db[item_id], "id": item_id}
    except ItemNotFoundException:
        raise
    except ItemNotFoundException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving item {item_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving item"
        )

# Users endpoints
@app.get("/users/")
async def get_users():
    """Get all users"""
    try:
        if not users_db:
            logger.info("Retrieving empty users list")
            return {"users": [], "count": 0}
        logger.info(f"Retrieved {len(users_db)} users")
        return {"users": users_db, "count": len(users_db)}
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving users"
        )

@app.post("/users/")
async def create_user(user: User):
    """Create a new user"""
    try:
        # Validate email format
        if "@" not in user.email or "." not in user.email:
            logger.warning(f"Invalid email format: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Validate name
        if not user.name or len(user.name.strip()) == 0:
            logger.warning("Attempted to create user with empty name")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User name cannot be empty"
            )
        
        # Validate age if provided
        if user.age is not None and user.age < 0:
            logger.warning(f"Invalid age: {user.age}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Age cannot be negative"
            )
        
        user_dict = user.dict()
        users_db.append(user_dict)
        logger.info(f"User created: {user.name} ({user.email})")
        return {
            "message": "User created successfully",
            "user": user_dict,
            "total_users": len(users_db)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred while creating user"
        )

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get a specific user by ID"""
    try:
        # Validate user_id
        if user_id < 0:
            logger.warning(f"Attempted to get user with negative ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID cannot be negative"
            )
        
        if user_id >= len(users_db):
            logger.warning(f"User not found: ID {user_id}")
            raise UserNotFoundException(user_id)
        
        logger.info(f"Retrieved user ID: {user_id}")
        return {"user": users_db[user_id], "id": user_id}
    except UserNotFoundException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user"
        )

# Health check
@app.get("/health/")
async def health_check():
    """Health check endpoint"""
    try:
        logger.info("Health check performed")
        return {
            "status": "healthy",
            "items_count": len(items_db),
            "users_count": len(users_db)
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
