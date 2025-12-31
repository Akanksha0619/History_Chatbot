from fastapi import APIRouter
from models.user import UserCreate, UserUpdate
from utils.user import (
    create_user_util,
    get_user_util,
    update_user_util,
    delete_user_util
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(user: UserCreate):
    return create_user_util(user)


@router.get("/{user_id}")
def get_user(user_id: str):
    return get_user_util(user_id)


@router.put("/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    return update_user_util(user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: str):
    return delete_user_util(user_id)
