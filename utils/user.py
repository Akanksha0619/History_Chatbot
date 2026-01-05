from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException, status
from models.response import APIResponse
from models.user import UserCreate, UserUpdate
from services.user import (
    create_user_db,
    get_user_db,
    update_user_db,
    delete_user_db,
    get_all_users_db
)

def _get_user_or_404(user_id: str):
    doc = get_user_db(user_id)
    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return doc


def create_user(user: UserCreate) -> APIResponse:
    user_id = str(uuid4())

    data = {
        "id": user_id,
        "name": user.name,
        "created_at": datetime.utcnow().isoformat()
    }

    create_user_db(user_id, data)

    return APIResponse(
        success=True,
        message="User created successfully",
        data={"id": user_id}
    )


def get_all_users() -> APIResponse:
    users = get_all_users_db()

    if not users:
        return APIResponse(
            success=True,
            message="No users found",
            data=[]
        )

    return APIResponse(
        success=True,
        message="Users fetched successfully",
        data=users
    )


def get_user(user_id: str) -> APIResponse:
    doc = _get_user_or_404(user_id)

    return APIResponse(
        success=True,
        data=doc.to_dict()
    )


def update_user(user_id: str, user: UserUpdate) -> APIResponse:
    _get_user_or_404(user_id)

    update_data = {
        k: v for k, v in user.model_dump().items()
        if v is not None
    }

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data to update"
        )

    update_user_db(user_id, update_data)

    return APIResponse(
        success=True,
        message="User updated successfully"
    )


def delete_user(user_id: str) -> APIResponse:
    _get_user_or_404(user_id)

    delete_user_db(user_id)

    return APIResponse(
        success=True,
        message="User deleted successfully"
    )
