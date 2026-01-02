from datetime import datetime
from database.db import db
from config.config import client
from firebase_admin import firestore


def get_last_messages(conversation_id: str, limit: int = 15):
    docs = (
        db.collection("conversations")
        .document(conversation_id)
        .collection("messages")
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )

    messages = []
    for doc in docs:
        data = doc.to_dict()
        messages.append({
            "role": data["role"],
            "content": data["content"]
        })

    return list(reversed(messages))  


def save_message(conversation_id: str, role: str, content: str):
    db.collection("conversations") \
      .document(conversation_id) \
      .collection("messages") \
      .add({
          "role": role,
          "content": content,
          "created_at": datetime.utcnow()
      })


def ai_reply(conversation_id: str, user_message: str) -> str:
    history = get_last_messages(conversation_id)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer based on previous conversation."
        }
    ]

    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    # 🔹 Save messages
    save_message(conversation_id, "user", user_message)
    save_message(conversation_id, "assistant", reply)

    return reply
