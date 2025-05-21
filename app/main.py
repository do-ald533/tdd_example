from fastapi import FastAPI
from app.api import auth

app = FastAPI(
    title="User Authentication API",
    description="A TDD example for user authentication with FastAPI",
    version="0.1.0"
)


app.include_router(auth.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the User Authentication API"}
