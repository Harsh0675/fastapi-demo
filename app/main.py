from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routes.auth import router as auth_router
from .routes.users import router as users_router

app = FastAPI(
    title="Termux REST API",
    version="2.0.0",
    description="FastAPI + SQLite + JWT authentication backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", tags=["System"])
def home():
    return {
        "message": "🚀 Termux API is running",
        "database": "SQLite",
        "authentication": "JWT",
        "status": "online",
    }
