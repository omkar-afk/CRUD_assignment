# FastAPI MongoDB CRUD Application

A simple REST API implementing CRUD operations using FastAPI and MongoDB.

## Prerequisites

- Python 3.7+
- MongoDB
- pip (Python package installer)

## Environment Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a `.env` file and add:
```
MONGO_DETAILS="mongodb://localhost:27017"
```

## Running the Application

```bash
uvicorn app.app:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Welcome message
- `POST /user`: Create new user
- `GET /user/{id}`: Get user by ID
- `GET /users`: List all users
- `PUT /user/{id}`: Update user
- `DELETE /user/{id}`: Delete user

## Data Model

```python
User {
    name: string
    email: string
}
```

