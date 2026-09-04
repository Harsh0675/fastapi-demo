import sqlite3

from fastapi import APIRouter, HTTPException

from .. import models
from ..schemas import User, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=User, status_code=201)
def create_user(user: UserCreate):
    try:
        return models.create_user(user.name, str(user.email))
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )


@router.get("", response_model=list[User])
def list_users():
    return models.get_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = models.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate):
    try:
        result = models.update_user(
            user_id,
            user.name,
            str(user.email)
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return result


@router.delete("/{user_id}")
def delete_user(user_id: int):
    deleted = models.delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully",
        "id": user_id
    }
