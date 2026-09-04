import sqlite3

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from ..database import get_db
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Authentication"])

security = HTTPBearer()


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", status_code=201)
def register(data: RegisterRequest):
    if len(data.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters"
        )

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (
                data.name,
                str(data.email),
                hash_password(data.password),
            ),
        )

        conn.commit()

        return {
            "id": cursor.lastrowid,
            "name": data.name,
            "email": str(data.email),
            "message": "Registration successful",
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    finally:
        conn.close()


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    conn = get_db()

    row = conn.execute(
        """
        SELECT id, password_hash
        FROM users
        WHERE email = ?
        """,
        (str(data.email),),
    ).fetchone()

    conn.close()

    if row is None or not row["password_hash"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(data.password, row["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(row["id"])

    return {
        "access_token": token,
        "token_type": "bearer",
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        user_id = decode_access_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    conn = get_db()

    user = conn.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()

    conn.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return dict(user)


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user
