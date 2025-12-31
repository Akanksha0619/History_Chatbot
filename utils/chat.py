from uuid import uuid4
from datetime import datetime
from database.db import db
from config.chat_service import ai_reply
from firebase_admin import firestore


def handle_chat(req):
    now = datetime.utcnow().isoformat()

    # 🔹 Get or Create Conversation
    conversation_id = req.conversation_id or str(uuid4())
    conv_ref = db.collection("conversations").document(conversation_id)
    conv_doc = conv_ref.get()

    if not conv_doc.exists:
        conv_ref.set({
            "conversation_id": conversation_id,
            "user_id": req.user_id,
            "messages": [],
            "created_at": now,
            "updated_at": now
        })

    # 🔹 User Message
    user_message = {
        "role": "user",
        "text": req.message,
        "time": now
    }

    # 🔹 AI Reply
    reply = ai_reply(req.message)

    ai_message = {
        "role": "assistant",
        "text": reply,
        "time": now
    }

    # 🔹 Single Firestore Update
    conv_ref.update({
        "messages": firestore.ArrayUnion([user_message, ai_message]),
        "updated_at": now
    })

    return {
        "conversation_id": conversation_id,
        "reply": reply
    }
