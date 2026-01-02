from services.db import db

COLLECTION = "client"


def create_user_db(user_id: str, data: dict):
    db.collection(COLLECTION).document(user_id).set(data)
    return data


def get_user_db(user_id: str):
    doc = db.collection(COLLECTION).document(user_id).get()
    return doc


def update_user_db(user_id: str, update_data: dict):
    doc_ref = db.collection(COLLECTION).document(user_id)
    doc_ref.update(update_data)


def delete_user_db(user_id: str):
    doc_ref = db.collection(COLLECTION).document(user_id)
    doc_ref.delete()
