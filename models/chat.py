from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    user_id: str = Field(..., example="user_123")
    message: str = Field(..., min_length=1, example="My name is Akanksha")
    conversation_id: Optional[str] = Field(None, example="conversation_123")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "message": "What is my name?",
                "conversation_id": "conversation_123"
            }
        }
