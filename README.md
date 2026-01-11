# FastAPI Sample Project

A simple FastAPI project demonstrating basic CRUD operations for items and users.

## Features

- **Items Management**: Create and retrieve items with name, description, price, and tax
- **Users Management**: Create and retrieve users with name, email, and age
- **Health Check**: Built-in health check endpoint
- **Interactive API Docs**: Automatic Swagger UI and ReDoc documentation

## Project Structure

```
fast api project/
├── main.py              # Main FastAPI application
├── requirements.txt     # Project dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## Installation

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the FastAPI development server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### General
- `GET /` - Welcome message
- `GET /health/` - Health check

### Items
- `GET /items/` - Get all items
- `POST /items/` - Create a new item
- `GET /items/{item_id}` - Get a specific item

### Users
- `GET /users/` - Get all users
- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get a specific user

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Requests

### Create an Item
```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"A powerful laptop","price":999.99,"tax":100}'
```

### Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","age":30}'
```

### Get All Items
```bash
curl "http://localhost:8000/items/"
```

### Get All Users
```bash
curl "http://localhost:8000/users/"
```

## Technologies Used

- **FastAPI**: Modern Python web framework for building APIs
- **Uvicorn**: ASGI web server
- **Pydantic**: Data validation using Python type annotations

## Next Steps

- Add database integration (SQLAlchemy, MongoDB, etc.)
- Implement authentication and authorization
- Add request validation and error handling
- Create unit and integration tests
- Deploy to production (Docker, cloud platforms, etc.)
