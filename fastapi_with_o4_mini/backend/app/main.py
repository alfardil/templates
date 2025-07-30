"""Main entry point for the FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import generate

app = FastAPI()
app.include_router(generate.router)


# add public frontend url later for cors
origins = ["http://localhost:3000", "http://localhost:5173"]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root API for the project."""
    return {
        "message": "Welcome to the API for this project.",
        "contributors": ["Alfardil Alam", "Abid Ali"],
    }
