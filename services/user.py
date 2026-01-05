from config.db import db

COLLECTION = "client"


def create_user_db(user_id: str, data: dict):
    db.collection(COLLECTION).document(user_id).set(data)


def get_all_users_db():
    docs = db.collection(COLLECTION).stream()

    users = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        users.append(data)

    return users


def get_user_db(user_id: str):
    return db.collection(COLLECTION).document(user_id).get()


def update_user_db(user_id: str, update_data: dict):
    db.collection(COLLECTION).document(user_id).update(update_data)


def delete_user_db(user_id: str):
    db.collection(COLLECTION).document(user_id).delete()

