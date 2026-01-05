from uuid import uuid4
from datetime import datetime
from config.db import db
from config.config import client
from fastapi import HTTPException, status
from models.response import APIResponse   


def process_chat(
    user_id: str,
    message: str,
    conversation_id: str | None = None
):
    try:
        now = datetime.utcnow().isoformat()

        if not conversation_id:
            conversation_id = str(uuid4())

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
            {"role": "user", "content": message},
            {"role": "assistant", "content": reply}
        ])

        conv_ref.update({
            "messages": history,
            "updated_at": datetime.utcnow().isoformat()
        })

    
        return APIResponse(
            success=True,
            message="Chat processed successfully",
            data={
                "conversation_id": conversation_id,
                "reply": reply
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
