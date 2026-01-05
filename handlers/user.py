from fastapi import APIRouter
from models.user import UserCreate, UserUpdate
from models.auth import LoginRequest
from utils.user import (
    create_user,
    get_user,
    update_user,
    delete_user,
    get_all_users,
    
)

router = APIRouter()


@router.post("/")
def create_user_api(user: UserCreate):
    return create_user(user)


@router.get("/")
def get_users():
    return get_all_users()


@router.get("/{user_id}")
def get_user_api(user_id: str):
    return get_user(user_id)


@router.put("/{user_id}")
def update_user_api(user_id: str, user: UserUpdate):
    return update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user_api(user_id: str):
    return delete_user(user_id)


