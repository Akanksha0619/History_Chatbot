from fastapi import HTTPException, status
from models.response import APIResponse
from services.user import get_user_by_email_db
from services.security import verify_password


def login_user(email: str, password: str) -> APIResponse:
    user = get_user_by_email_db(email)

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
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
