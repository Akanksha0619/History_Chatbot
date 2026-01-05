from config.db import db

COLLECTION = "client"


def create_user_db(user_id: str, data: dict):
    db.collection(COLLECTION).document(user_id).set(data)


def get_user_db(user_id: str):
    return db.collection(COLLECTION).document(user_id).get()


def update_user_db(user_id: str, data: dict):
    db.collection(COLLECTION).document(user_id).update(data)


def delete_user_db(user_id: str):
    db.collection(COLLECTION).document(user_id).delete()


def get_all_users_db():
    docs = db.collection(COLLECTION).stream()
    return [doc.to_dict() for doc in docs]


def get_user_by_email_db(email: str):
    docs = (
        db.collection(COLLECTION)
        .where("email", "==", email)
        .limit(1)
        .stream()
    )
    for doc in docs:
        return doc.to_dict()
    return None
