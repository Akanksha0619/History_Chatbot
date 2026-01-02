from uuid import uuid4
from datetime import datetime
from firebase_admin import firestore
from services.db import db
from config.config import client


def process_chat(
    user_id: str,
    message: str,
    conversation_id: str | None = None
):
    now = datetime.utcnow().isoformat()

 
    conversation_id = conversation_id or str(uuid4())
    conv_ref = db.collection("conversations").document(conversation_id)
    conv_doc = conv_ref.get()

    if not conv_doc.exists:
        conversation = {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "messages": [],
            "created_at": now,
            "updated_at": now
        }
        conv_ref.set(conversation)
        history = []
    else:
        conversation = conv_doc.to_dict()
        history = conversation.get("messages", [])


    messages_for_ai = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Use previous conversation if available."
        }
    ]

    for msg in history[-15:]:
        messages_for_ai.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages_for_ai.append({
        "role": "user",
        "content": message
    })

   
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages_for_ai
    )

    reply = response.choices[0].message.content

   
    history.extend([
        {
            "role": "user",
            "content": message,
            "time": now
        },
        {
            "role": "assistant",
            "content": reply,
            "time": now
        }
    ])

   
    conv_ref.update({
        "messages": history,
        "updated_at": now
    })

    return {
        "conversation_id": conversation_id,
        "reply": reply
    }
