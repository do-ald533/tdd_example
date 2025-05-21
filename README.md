# User Authentication TDD Example

This project demonstrates Test-Driven Development (TDD) principles applied to user authentication functionality (registration and login) using Python, FastAPI, and pytest.

## Project Structure

```
app/
├── api/            # API routes and endpoints
├── models/         # Pydantic models for request/response
├── services/       # Business logic
├── repositories/   # Data access layer
└── tests/          # Test files
```

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running Tests

Run the tests using pytest:

```
pytest
```

To see test coverage:

```
pytest --cov=app
```

## Running the Application

Start the FastAPI application:

```
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

API documentation will be available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
