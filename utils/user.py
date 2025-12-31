from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from database.db import db

COLLECTION = "client"


def create_user_util(user):
    user_id = str(uuid4())

    data = {
        "id": user_id,
        "name": user.name,
        "created_at": datetime.utcnow().isoformat()
    }

    db.collection(COLLECTION).document(user_id).set(data)
    return data


def get_user_util(user_id: str):
    doc = db.collection(COLLECTION).document(user_id).get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    return doc.to_dict()


def update_user_util(user_id: str, user):
    doc_ref = db.collection(COLLECTION).document(user_id)

    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {
        k: v for k, v in user.model_dump().items() if v is not None
    }

    doc_ref.update(update_data)

    return {"message": "User updated successfully"}


def delete_user_util(user_id: str):
    doc_ref = db.collection(COLLECTION).document(user_id)

    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="User not found")

    doc_ref.delete()

    return {"message": "User deleted successfully"}
