from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from models.response import APIResponse
from models.user import UserCreate, UserUpdate
from services.security import hash_password, verify_password
from services.user import (
    create_user_db,
    get_user_db,
    update_user_db,
    delete_user_db,
    get_all_users_db,
    get_user_by_email_db
)



def create_user(user: UserCreate) -> APIResponse:
    try:
        if not user.name or not user.email or not user.password:
            return APIResponse(success=False, message="Missing required fields", data={}
            )

        if get_user_by_email_db(user.email):
            return APIResponse(
                success=False,
                message="Email already registered",
                data={}
            )

        user_id = str(uuid4())

        data = {
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "password": hash_password(user.password),
            "created_at": datetime.utcnow().isoformat()
        }

        create_user_db(user_id, data)

        return APIResponse(
            success=True,
            message="User created successfully",
            data={"id": user_id}
        )

    except ValidationError as e:
        return APIResponse(
            success=False,
            message="Invalid user data",
            data=e.errors()
        )

    except Exception as e:
        return APIResponse(
            success=False,
            message="Failed to create user",
            data=str(e)
        )



def get_all_users() -> APIResponse:
    users = get_all_users_db()

    return APIResponse(
        success=True,
        message="Users fetched successfully",
        data=users or []
    )


def get_user(user_id: str) -> APIResponse:
    doc = get_user_db(user_id)

    if not doc.exists:
        return APIResponse(
            success=False,
            message="User not found"
        )

    user_data = doc.to_dict()
    user_data.pop("password", None)

    return APIResponse(
        success=True,
        data=user_data
    )


def update_user(user_id: str, user: UserUpdate) -> APIResponse:
    doc = get_user_db(user_id)

    if not doc.exists:
        return APIResponse(
            success=False,
            message="User not found"
        )

    update_data = {
        key: value
        for key, value in user.model_dump().items()
        if value is not None and key != "password"
    }

    if user.password:
        update_data["password"] = hash_password(user.password)

    if not update_data:
        return APIResponse(
            success=False,
            message="No data to update"
        )

    update_user_db(user_id, update_data)

    return APIResponse(
        success=True,
        message="User updated successfully",
        data={"id": user_id}
    )


def delete_user(user_id: str) -> APIResponse:
    doc = get_user_db(user_id)

    if not doc.exists:
        return APIResponse(
            success=False,
            message="User not found"
        )

    delete_user_db(user_id)

    return APIResponse(
        success=True,
        message="User deleted successfully"
    )


def login_user(email: str, password: str) -> APIResponse:
    user = get_user_by_email_db(email)

    if not user:
        return APIResponse(
            success=False,
            message="Invalid email or password"
        )

    if not verify_password(password, user["password"]):
        return APIResponse(
            success=False,
            message="Invalid email or password"
        )

    return APIResponse(
        success=True,
        message="Login successful",
        data={
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    )
