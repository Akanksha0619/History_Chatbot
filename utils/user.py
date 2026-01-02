from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from services.user import (
    create_user_db,
    get_user_db,
    update_user_db,
    delete_user_db
)


def create_user(user):
    user_id = str(uuid4())

    data = {
        "id": user_id,
        "name": user.name,
        "created_at": datetime.utcnow().isoformat()
    }

    return create_user_db(user_id, data)


def get_user(user_id: str):
    doc = get_user_db(user_id)

    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    return doc.to_dict()


def update_user(user_id: str, user):
    doc = get_user_db(user_id)

    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {
        k: v for k, v in user.model_dump().items()
        if v is not None
    }

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    update_user_db(user_id, update_data)

    return {"message": "User updated successfully"}


def delete_user(user_id: str):
    doc = get_user_db(user_id)

    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    delete_user_db(user_id)

    return {"message": "User deleted successfully"}
